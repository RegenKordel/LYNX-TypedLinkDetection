from tensorflow.keras.backend import expand_dims
from tensorflow.keras.layers import Conv2D, BatchNormalization, Reshape, MaxPooling2D, Flatten, Concatenate, Input
from tensorflow.keras.models import Model


def build_sccnn_model(max_seq_length: int):
    text_in = Input(shape=(max_seq_length, 20, 2), dtype='float32', name='Text_Input')

    issue_model = build_issue_model(max_seq_length)
    encoded_issue_a = issue_model([text_in[..., 0]])
    encoded_issue_b = issue_model([text_in[..., 1]])

    encoded_link = Concatenate()([encoded_issue_a, encoded_issue_b])

    return Model(inputs=[text_in], outputs=encoded_link)


def build_issue_model(max_seq_length: int):
    text_in = Input(shape=(max_seq_length, 20), dtype='float32', name='Text_Input')
    x = expand_dims(text_in, axis=-1)

    A = build_branch_a(x, max_seq_length=max_seq_length)
    B = build_branch_b(x, max_seq_length=max_seq_length)
    C = build_branch_c(x, max_seq_length=max_seq_length)

    conv_concat = Concatenate(axis=-1)([A, B])
    conv_concat = Concatenate(axis=-1)([conv_concat, C])

    return Model(inputs=[text_in], outputs=[conv_concat], name='SC-CNN_Model')


def build_branch_a(text_in, max_seq_length: int):
    conv_a = Conv2D(
        filters=100,
        kernel_size=(2, 20),
        strides=(1, 1),
        activation='relu',
        name="BranchA"
    )(text_in)

    conv_a = BatchNormalization(axis=-1)(conv_a)

    conv_a_rs = Reshape((max_seq_length - 1, 100, 1))(conv_a)

    conv_a_1 = Conv2D(
        filters=200,
        kernel_size=(2, 100),
        strides=(1, 1),
        activation='relu',
        name="BranchA1"
    )(conv_a_rs)

    pooled_conv_a_1 = MaxPooling2D(pool_size=(conv_a_1.shape[1], 1), padding='valid')(conv_a_1)
    pooled_conv_a_1 = Flatten()(pooled_conv_a_1)

    conv_a_2 = Conv2D(
        filters=200,
        kernel_size=(3, 100),
        activation='relu',
        strides=(1, 1),
        name="BranchA2"
    )(conv_a_rs)

    pooled_conv_a_2 = MaxPooling2D(pool_size=(conv_a_2.shape[1], 1), padding='valid')(conv_a_2)
    pooled_conv_a_2 = Flatten()(pooled_conv_a_2)

    conv_a_3 = Conv2D(
        filters=200,
        kernel_size=(4, 100),
        activation='relu',
        strides=(1, 1),
        name="BranchA3"
    )(conv_a_rs)

    pooled_conv_a_3 = MaxPooling2D(pool_size=(conv_a_3.shape[1], 1), padding='valid')(conv_a_3)
    pooled_conv_a_3 = Flatten()(pooled_conv_a_3)

    A = Concatenate(axis=-1)([pooled_conv_a_1, pooled_conv_a_2])
    A = Concatenate(axis=-1)([A, pooled_conv_a_3])
    return A


def build_branch_b(text_in, max_seq_length: int):
    conv_b = Conv2D(
        filters=100,
        kernel_size=(3, 20),
        activation='relu',
        strides=(1, 1),
        name="BranchB"
    )(text_in)

    conv_b = BatchNormalization(axis=-1)(conv_b)

    conv_b_rs = Reshape((max_seq_length - 2, 100, 1))(conv_b)

    conv_b_1 = Conv2D(
        filters=200,
        kernel_size=(2, 100),
        activation='relu',
        strides=(1, 1),
        name="BranchB1"
    )(conv_b_rs)

    pooled_conv_b_1 = MaxPooling2D(pool_size=(conv_b_1.shape[1], 1), padding='valid')(conv_b_1)
    pooled_conv_b_1 = Flatten()(pooled_conv_b_1)

    conv_b_2 = Conv2D(
        filters=200,
        kernel_size=(3, 100),
        activation='relu',
        strides=(1, 1),
        name="BranchB2"
    )(conv_b_rs)

    pooled_conv_b_2 = MaxPooling2D(pool_size=(conv_b_2.shape[1], 1), padding='valid')(conv_b_2)
    pooled_conv_b_2 = Flatten()(pooled_conv_b_2)

    conv_b_3 = Conv2D(
        filters=200,
        kernel_size=(4, 100),
        activation='relu',
        strides=(1, 1),
        name="BranchB3"
    )(conv_b_rs)

    pooled_conv_b_3 = MaxPooling2D(pool_size=(conv_b_3.shape[1], 1), padding='valid')(conv_b_3)
    pooled_conv_b_3 = Flatten()(pooled_conv_b_3)

    B = Concatenate(axis=-1)([pooled_conv_b_1, pooled_conv_b_2])
    B = Concatenate(axis=-1)([B, pooled_conv_b_3])
    return B


def build_branch_c(text_in, max_seq_length: int):
    conv_c = Conv2D(
        filters=100,
        kernel_size=(4, 20),
        activation='relu',
        strides=(1, 1),
        name="BranchC"
    )(text_in)
    conv_c = BatchNormalization(axis=-1)(conv_c)

    conv_c_rs = Reshape((max_seq_length - 3, 100, 1))(conv_c)

    conv_c_1 = Conv2D(
        filters=200,
        kernel_size=(2, 100),
        activation='relu',
        strides=(1, 1),
        name="BranchC1"
    )(conv_c_rs)

    pooled_conv_c_1 = MaxPooling2D(pool_size=(conv_c_1.shape[1], 1), padding='valid')(conv_c_1)
    pooled_conv_c_1 = Flatten()(pooled_conv_c_1)

    conv_c_2 = Conv2D(
        filters=200,
        kernel_size=(3, 100),
        activation='relu',
        strides=(1, 1),
        name="BranchC2"
    )(conv_c_rs)

    pooled_conv_c_2 = MaxPooling2D(pool_size=(conv_c_2.shape[1], 1), padding='valid')(conv_c_2)
    pooled_conv_c_2 = Flatten()(pooled_conv_c_2)

    conv_c_3 = Conv2D(
        filters=200,
        kernel_size=(4, 100),
        activation='relu',
        strides=(1, 1),
        name="BranchC3"
    )(conv_c_rs)

    pooled_conv_c_3 = MaxPooling2D(pool_size=(conv_c_3.shape[1], 1), padding='valid')(conv_c_3)
    pooled_conv_c_3 = Flatten()(pooled_conv_c_3)

    C = Concatenate(axis=-1)([pooled_conv_c_1, pooled_conv_c_2])
    C = Concatenate(axis=-1)([C, pooled_conv_c_3])
    return C
