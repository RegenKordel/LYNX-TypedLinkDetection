from typing import Protocol

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_addons as tfa
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model

from tld.config import train_results_dir, link_embedding_dir
from tld.models.cnn.data import WordEmbeddingModelName, get_label_to_linktype_map, load_issues, load_links, \
    prepare_links, load_word_ids, add_word_ids, calc_max_concat_seq_length, build_embedding_model, \
    load_embedding_matrix, train_classifier, get_link_embeddings
from tld.models.cnn.shared import assemble_models


class LinkModelBuilder(Protocol):
    def __call__(self, max_seq_length: int) -> Model: ...


def main(model_name: str, build_link_model: LinkModelBuilder, source: str, include_non_links: bool):
    tf.compat.v1.disable_eager_execution()

    issue_df = load_issues(source)

    link_df = load_links(source, include_non_links=include_non_links)
    link_df = prepare_links(link_df)
    label_to_linktype = get_label_to_linktype_map(link_df)

    embedding_model_name: WordEmbeddingModelName = 'w2v'
    issue_df['text_emb'] = list(load_word_ids(embedding_model_name, source=source))
    train_df, test_df = train_test_split(
        add_word_ids(link_df=link_df, issue_df=issue_df),
        test_size=0.2,
        random_state=9,
    )

    max_sequence_length = calc_max_concat_seq_length(issue_df)

    embedding_model = build_embedding_model(
        embedding_matrix=load_embedding_matrix(embedding_model_name, source=source),
        max_seq_length=max_sequence_length,
    )

    inner_model = build_link_model(max_seq_length=max_sequence_length)
    model = assemble_models(
        word_embedding_model=embedding_model,
        link_model=inner_model,
        max_seq_length=max_sequence_length,
    )
    train_model(model=model, dataset=train_df)

    clf = RandomForestClassifier(max_depth=25, random_state=0)
    train_classifier(classifier=clf, link_embedder=model, train_df=train_df)

    results_test = get_link_embeddings(model, test_df)
    test_df['preds'] = clf.predict(results_test)

    class_rep = classification_report(
        test_df['label'],
        test_df['preds'],
        output_dict=True,
        target_names=[linktype for label, linktype in sorted(label_to_linktype.items())],
    )

    class_rep_df = pd.DataFrame(class_rep).transpose()

    conf_mat = confusion_matrix(test_df['preds'], test_df['label'])
    conf_mat_df = pd.DataFrame(conf_mat).transpose()
    conf_mat_df.rename(index=label_to_linktype, inplace=True)
    conf_mat_df.rename(columns=label_to_linktype, inplace=True)

    configuration_key = f'{source}_LT' + ('_plus' if include_non_links else '')
    test_df[['name', 'linktype', 'issue_id_1', 'issue_id_2', 'mappedtype', 'label', 'preds']] \
        .to_csv(link_embedding_dir / f'test_df_LT_{configuration_key}_{model_name}.csv')
    class_rep_df.to_csv(train_results_dir / f'class_rep_LT_{configuration_key}_{model_name}.csv')
    conf_mat_df.to_csv(train_results_dir / f'conf_mat_LT_{configuration_key}_{model_name}.csv')


def train_model(model, dataset):
    callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, verbose=2)

    model.compile(
        optimizer='adam',
        loss=tfa.losses.TripletSemiHardLoss()
    )

    train_issue_1 = dataset['text_emb_1']
    train_issue_1 = np.array(train_issue_1.values.tolist())

    train_issue_2 = dataset['text_emb_2']
    train_issue_2 = np.array(train_issue_2.values.tolist())

    model.fit(
        [train_issue_1, train_issue_2],
        y=dataset['label'],
        callbacks=[callback],
        validation_split=0.1,
        batch_size=128,
        epochs=64,
        verbose=2
    )
