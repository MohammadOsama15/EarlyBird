import h5py
import json
from keras.preprocessing.text import Tokenizer, tokenizer_from_json
from keras.utils import pad_sequences
from keras.models import load_model

MAX_LENGTH = 100
PADDING_TYPE = 'post'
TRUNCATION_TYPE = 'post'


model = load_model("model.h5")
with open('tokens.json') as f:
    data = json.load(f)
    Tokenizer = tokenizer_from_json(data)

model.summary()


def tokenize_sequence(text: list):
    """
    This function tokenizes input text and generated numeric vectors of uniform length

    Params:
        text: a list consisting of strings
    Returns:
        list
    """
    token_sequence = Tokenizer.texts_to_sequences(text)
    # pad or truncate sequences to achieve uniformity, note that 100 matches GloVe dataset dimension used for embedding
    token_padded = pad_sequences(
        token_sequence, maxlen=MAX_LENGTH, padding=PADDING_TYPE, truncating=TRUNCATION_TYPE)
    return token_padded
