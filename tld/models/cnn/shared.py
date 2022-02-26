from tensorflow.keras.layers import BatchNormalization, Reshape, Concatenate, Dropout, Dense, Input
from tensorflow.keras.models import Model


def assemble_models(word_embedding_model, link_model, max_seq_length: int):
    text_in_a = Input(shape=(max_seq_length,), dtype='int32', name="Text_issue_a")
    text_in_b = Input(shape=(max_seq_length,), dtype='int32', name="Text_issue_b")

    reshape = Reshape((max_seq_length, 20, 1))
    embeddings_a = reshape(word_embedding_model([text_in_a]))
    embeddings_b = reshape(word_embedding_model([text_in_b]))

    x = Concatenate(axis=-1)([embeddings_a, embeddings_b])

    x = link_model([x])

    x = Dropout(0.5)(x)
    x = Dense(units=512, activation='relu')(x)
    x = BatchNormalization(axis=-1)(x)

    x = Dropout(0.5)(x)
    x = Dense(units=256, activation='relu')(x)
    x = BatchNormalization(axis=-1)(x)

    x = Dropout(0.5)(x)
    x = Dense(units=128, activation='relu')(x)
    x = BatchNormalization(axis=-1)(x)

    x = Dropout(0.5)(x)
    x = Dense(units=64, activation='relu')(x)
    x = BatchNormalization(axis=-1)(x)

    return Model(inputs=[text_in_a, text_in_b], outputs=x)
