import h5py
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras_preprocessing.text import Tokenizer, tokenizer_from_json
from keras_preprocessing.sequence import pad_sequences
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
from tensorflow.keras.models import load_model
model = load_model("model.h5")
print(model.summary())
data = [["i ate bread this morning"], ["I am having a bad day, but that made me feel better"], ["bitter sweet"], ["charlie bit me!"], ["what a lovely day"], ["what a lovely day it is to die!"], ["chinese balloon has been detected again!"],
        ["she is so hateful"], ["that car is blue, and it's missing two wheels"], ["he stole the car and crashed it shortly after"], ["I am suffering from allergies"], ['Laika pooped on the carpet again'], ["russians are evil, they are eating goats"], ["chocolate taste sweet, so does honey"], ["John punched bob in the face and ran off"], ["John drank mangonada; then he had diarrhea"], ["sky is blue, and so are you"]]
df = pd.DataFrame(data)

with open('tokens.json') as f:
    data = json.load(f)
    Tokenizer = tokenizer_from_json(data)

X = df[0]

# generate encoded string
X_train_sequences = Tokenizer.texts_to_sequences(X)

# pad or truncate sequences to achieve uniformity, note that 100 matches GloVe dataset dimension used for embedding
max_length = 100
padding_type = 'post'
truncation_type = 'post'
X_test_padded = pad_sequences(
    X_train_sequences, maxlen=max_length, padding=padding_type, truncating=truncation_type)
predictions = model.predict(X_test_padded)
for item1, item2 in zip(X, predictions):
    print(item1, ": ", item2)
