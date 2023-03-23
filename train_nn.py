import io
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras_preprocessing.text import tokenizer_from_json
from keras_preprocessing.sequence import pad_sequences
from keras import Sequential
from keras.layers import Embedding, LSTM, Dense, Bidirectional
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import load_model

# import dataframe
df = pd.read_csv("sentiment140_trimmed.csv")
# extract tweet
X = df['tweet']
# extract label
y = df['sentiment']
# split training / testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)

checkpoint_path = "model.h5"
max_length = 100
# load model if one exists, else create and compile model
if checkpoint_path is not None:
    model = load_model("model.h5")
    with open('tokens.json') as f:
        data = json.load(f)
        Tokenizer = tokenizer_from_json(data)
else:
    # max num of tokens
    vocab_size = 50000
    Tokenizer = Tokenizer(num_words=vocab_size)
    # tokenize corpus
    Tokenizer.fit_on_texts(X_train)
    # word to num index
    word_index = Tokenizer.word_index
    # export tokenizer
    tokenizer_json = Tokenizer.to_json()
    with io.open('tokenizer.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(tokenizer_json, ensure_ascii=False))
        # import GloVe file
        embeddings_index = {}
        f = open('glove.6B.100d.txt', encoding="utf-8")
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
        f.close()

        # generate embedding matrix using words found in GloVe vocabulary
        embedding_matrix = np.zeros((len(word_index) + 1, max_length))
        for word, i in word_index.items():
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector

        # generate embedding layer
        embedding_layer = Embedding(input_dim=len(word_index) + 1,
                                    output_dim=max_length,
                                    weights=[embedding_matrix],
                                    input_length=max_length,
                                    trainable=False)

        # add layers to nn
        model = Sequential([
            embedding_layer,
            Bidirectional(LSTM(150, return_sequences=True)),
            Bidirectional(LSTM(150)),
            Dense(128, activation='relu'),
            Dense(1, activation='sigmoid')
        ])

        model.compile(loss='binary_crossentropy',
                      optimizer=Adam(), metrics=['accuracy'])

# generate encoded string
X_train_sequences = Tokenizer.texts_to_sequences(X_train)
X_test_sequences = Tokenizer.texts_to_sequences(X_test)

# pad or truncate sequences to achieve uniformity
padding_type = 'post'
truncation_type = 'post'
X_test_padded = pad_sequences(
    X_test_sequences,
    maxlen=max_length,
    padding=padding_type,
    truncating=truncation_type)
X_train_padded = pad_sequences(
    X_train_sequences,
    maxlen=max_length,
    padding=padding_type,
    truncating=truncation_type)
# specify number of epochs
num_epochs = 30
# callbacks
early_stop = EarlyStopping(monitor='loss', patience=5, verbose=1)
# set checkpoint with overwrite criteria set to minimal loss
file = "model.h5"
checkpoint = ModelCheckpoint(
    file, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint, early_stop]
model.fit(
    X_train_padded,
    y_train,
    epochs=num_epochs,
    validation_data=(X_test_padded, y_test),
    callbacks=callbacks_list)
model.save("model_final.h5")


def eval(model):
    loss, accuracy = model.evaluate(X_test_padded, y_test)
    print('Test accuracy :', accuracy)
