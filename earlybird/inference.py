import json
import os
from keras.preprocessing.text import tokenizer_from_json
from keras.utils import pad_sequences
from keras.models import load_model

MAX_LENGTH = 100
PADDING_TYPE = 'post'
TRUNCATION_TYPE = 'post'

# suppress tensorflow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
module_dir = os.path.dirname(__file__)

model = load_model(module_dir+"/ml/model.h5")
with open(module_dir+'/ml/tokens.json') as f:
    data = json.load(f)
    Tokenizer = tokenizer_from_json(data)


def tokenize_sequence(text: list):
    """
    Converts string to tokenized sequence
    Params:
        text: a list consisting of strings
    Returns:
        list
    """
    token_sequence = Tokenizer.texts_to_sequences(text)
    token_padded = pad_sequences(
        token_sequence,
        maxlen=MAX_LENGTH,
        padding=PADDING_TYPE,
        truncating=TRUNCATION_TYPE)
    return token_padded
