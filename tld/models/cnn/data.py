from typing import Dict, Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.ensemble import RandomForestClassifier
from tensorflow.keras.initializers import Constant
from tensorflow.keras.layers import Embedding, Input
from tensorflow.keras.models import Model

from tld.config import preprocessed_data_dir, word_embedding_dir
from tld.linktypes import fine_linktype_map


# Issues


def load_issues(tracker: str):
    filename = preprocessed_data_dir / f'issues_{tracker.lower()}.csv'
    return pd.read_csv(filename, encoding="UTF-8", low_memory=False, index_col=['issue_id'], sep=";")


def calc_max_seq_len(texts: pd.Series, quantile: float = 0.95):
    lengths = (texts.str.count(' ')+1).fillna(0).astype(np.int)
    return lengths.quantile(quantile, interpolation='higher')


def calc_max_concat_seq_length(issue_df: pd.DataFrame) -> int:
    return calc_max_seq_len(issue_df['title']) + calc_max_seq_len(issue_df['description'])


# Links


def load_links(tracker: str, include_non_links: bool):
    base_name = 'links_plus' if include_non_links else 'links'
    filename = preprocessed_data_dir / f'{base_name}_{tracker.lower()}.csv'
    return pd.read_csv(filename, encoding="UTF-8", low_memory=False, index_col=0, sep=";")


def prepare_links(link_df: pd.DataFrame):
    # filter out infrequent linktypes and add 'label' column containing linktype ids (0, 1, 2, …)
    link_df['mappedtype'] = link_df['linktype'].map(fine_linktype_map)
    min_occurrences = len(link_df)*0.01
    linktypes = (link_df['mappedtype'].value_counts() >= min_occurrences) \
        .rename_axis('mappedtype') \
        .reset_index(name='included')

    included_linktypes = set(linktypes[linktypes['included']]['mappedtype'])
    all_data = link_df[(link_df["mappedtype"].isin(included_linktypes))]
    all_data['label'] = all_data['mappedtype'].factorize()[0].astype(int)
    return all_data


def get_label_to_linktype_map(link_df: pd.DataFrame) -> Dict[str, int]:
    category_id_df = link_df[['mappedtype', 'label']].drop_duplicates().sort_values('label')
    return dict(category_id_df[['label', 'mappedtype']].values)


# Embeddings


WordEmbeddingModelName = Literal['glove', 'w2v', 'fasttext']


def build_embedding_model(embedding_matrix: np.ndarray, max_seq_length: int):
    embedding_layer = Embedding(
        embedding_matrix.shape[0],
        embedding_matrix.shape[1],
        embeddings_initializer=Constant(embedding_matrix),
        input_length=max_seq_length,
        trainable=False,
    )
    # from keras.layers import concatenate
    text_in = Input(shape=(max_seq_length,), name='Text_Input')
    text_out = embedding_layer(text_in)

    return Model(inputs=[text_in], outputs=[text_out], name='Text_Output')


def load_word_ids(embedding_model: WordEmbeddingModelName, source: str) -> np.ndarray:
    return np.load(word_embedding_dir / embedding_model / f'text_data_{source}.npy')


def load_embedding_matrix(embedding_model: WordEmbeddingModelName, source: str):
    assert embedding_model == 'w2v'

    model = Word2Vec.load(str(word_embedding_dir / embedding_model / f'{source}W2V.model'))
    embedding_matrix = np.zeros((len(model.wv), model.wv.vector_size))
    for i in range(len(model.wv)):
        embedding_vector = model.wv[model.wv.index_to_key[i]]
        if embedding_vector is not None:
            embedding_matrix[i] = embedding_vector

    return embedding_matrix


def add_word_ids(link_df: pd.DataFrame, issue_df: pd.DataFrame):
    issue_feat_data = issue_df[['text_emb']]

    return link_df \
        .merge(issue_feat_data, left_on='issue_id_1', right_on='issue_id') \
        .merge(issue_feat_data, left_on='issue_id_2', right_on='issue_id', suffixes=('_1', '_2'))


# Processing


def train_classifier(classifier: RandomForestClassifier, link_embedder: Model, train_df: pd.DataFrame):
    results_train = get_link_embeddings(link_embedder, train_df)
    classifier.fit(results_train, train_df['label'])


def get_link_embeddings(link_embedding_model: Model, data_df: pd.DataFrame):
    issue_1 = np.array(data_df['text_emb_1'].values.tolist())
    issue_2 = np.array(data_df['text_emb_2'].values.tolist())
    return link_embedding_model.predict([issue_1, issue_2])


def plot_history(history):
    for i in list(history.history)[0:2]:
        print(i)
        # list all data in history
        # summarize history for accuracy
        plt.plot(history.history[i])
        plt.title('model ' + i)
        plt.ylabel(i)
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
