import keras
from keras.layers import Input, Embedding, BatchNormalization, Bidirectional, GRU, Concatenate, Dense, Reshape, Lambda
from keras.models import Model, Sequential
import keras.backend as K

import numpy as np
from .dictionary import vocab

MODEL_FILE = 'ner-20181105.hdf5'

def generate_model(vocab):
    inp = Input(shape=(None,))
    emb = Embedding(vocab.num_chars, 48, name='embedding', mask_zero=True)(inp)
    norm0 = BatchNormalization()(emb)

    rnn1 = Bidirectional(GRU(32, return_sequences=True, reset_after=True, recurrent_activation='sigmoid'))(norm0)
    res1 = BatchNormalization()(Concatenate()([norm0, rnn1]))

    rnn2 = Bidirectional(GRU(32, return_sequences=True, reset_after=True, recurrent_activation='sigmoid'))(res1)
    res2 = BatchNormalization()(Concatenate()([norm0, rnn2]))

    rnn3 = Bidirectional(GRU(32, return_sequences=True, reset_after=True, recurrent_activation='sigmoid'))(res2)
    res3 = BatchNormalization()(Concatenate()([norm0, rnn3]))
    con = Concatenate()([norm0, res3])

    fc1 = Dense(64, activation='relu')(con)
    fc2 = Dense(1, activation='sigmoid', name='fc')(fc1)

    # disable the masking
    fc2 = Lambda(lambda x: x, output_shape=lambda s:s)(fc2)
    out = Reshape((-1,))(fc2)

    return Model(inp, out)

model = generate_model(vocab)
model.load_weights(f'models/ner/{MODEL_FILE}')
model._make_predict_function()

print("NER model loaded, NN architecture shown below:")
model.summary()
