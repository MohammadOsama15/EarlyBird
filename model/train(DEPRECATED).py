#!/usr/bin/env python
# coding: utf-8

# # Training our model
# This code trains a model for predicting tweet sentiment using PyTorch, Pandas and the Sentiment140 dataset.
# 
# (**NOTE:** This code is N/A, we are using TensorFlow. See `tf_train.ipynb` for latest code.)

# In[83]:


import torch
import pandas as pd


# In[84]:


torch.__version__


# In[85]:


# Enable CUDA if available (GPU acceleration)
if torch.cuda.is_available():
    device = torch.device("cuda") 
else:
    device = torch.device("cpu")
    
device


# ## Formatting data

# In[86]:


# Load data
input_file = 'data/training.1600000.processed.noemoticon.csv'
df = pd.read_csv(input_file, header = None, encoding='latin1')


# In[87]:


df.shape


# In[88]:


df[0].value_counts()


# In[89]:


'''
    Columns are as follows:
    0. target: the polarity of the tweet (0 = negative, 4 = positive)
    1. ids: The id of the tweet
    2. date: the date of the tweet
    3. flag: The query. If there is no query, then this value is NO_QUERY.
    4. user: the user that tweeted
    5. text: the text of the tweet

'''
df.head()


# In[90]:


df.tail()


# ## Training model

# In[91]:


import torchtext
from torchtext import data
from sklearn.model_selection import train_test_split
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# In[92]:


torchtext.__version__


# ### Tokenization
# Preprocessing tweets with the SpaCy tokenizer to remove unnecessary parts, keeping only meaningful words/characters

# In[99]:


import re
from nltk.corpus import stopwords
from collections import Counter

def tokenize(x_train,y_train,x_val,y_val):
    word_list = []

    stop_words = set(stopwords.words('english')) 
    for sent in x_train:
        for word in sent.lower().split():
            word = preprocess_string(word)
            if word not in stop_words and word != '':
                word_list.append(word)
  
    corpus = Counter(word_list)
    corpus_ = sorted(corpus,key=corpus.get,reverse=True)[:1000]
    onehot_dict = {w:i+1 for i,w in enumerate(corpus_)}
    
    final_list_train,final_list_test = [],[]
    for sent in x_train:
            final_list_train.append([onehot_dict[preprocess_string(word)] for word in sent.lower().split() 
                                     if preprocess_string(word) in onehot_dict.keys()])
    for sent in x_val:
            final_list_test.append([onehot_dict[preprocess_string(word)] for word in sent.lower().split() 
                                    if preprocess_string(word) in onehot_dict.keys()])
            
    encoded_train = [1 if label =='positive' else 0 for label in y_train]  
    encoded_test = [1 if label =='positive' else 0 for label in y_val] 
    return np.array(final_list_train), np.array(encoded_train),np.array(final_list_test), np.array(encoded_test),onehot_dict

df_train = df[[0, 5]].copy().rename(columns={0:'sentiment', 5:'text'}) # Remove unnecessary columns and rename appropriately

regex_mentions = r"@[A-Za-z0-9_]+" # mentions
regex_links = r"https?://[A-Za-z0-9./]+" # links
regex_special = r"[^A-Za-z0-9]+" # special chars

df_train.text = df_train.text.apply(lambda x: re.sub(regex_mentions, " ", str(x).strip()))
df_train.text = df_train.text.apply(lambda x: re.sub(regex_links, " ", str(x).strip()))
df_train.text = df_train.text.apply(lambda x: re.sub(regex_special, " ", str(x).strip()))

x,y = df_train['text'].values, df_train['sentiment'].values # train-test split, x is input and y is output
x_train,x_test,y_train,y_test = train_test_split(x,y,stratify=y)
x_train,y_train,x_test,y_test,vocab = tokenize(x_train,y_train,x_test,y_test)


# In[100]:


print(f'Length of vocabulary is {len(vocab)}')


# In[120]:


print(len(x_test))


# In[115]:


print(y_test[int(len(y_test)/2)])


# In[101]:


df_train.head() # Results


# In[ ]:


print(f"Null values: \n\n{df_train.isna().sum()}")


# ### Prepare GLoVe word embedding vectors

# In[ ]:


embeddings_dictionary = dict()
embedding_dimension = 100
glove_file = open("data/glove.6B.50d.txt")

# Iterate through the glove file
for line in glove_file:
    # Split each line
    records = line.split()
    # Get the actual word
    word = records[0]
    # Get the dimensional representation
    representation = np.asarray(records[1:], dtype="float32")
    # Update the words dictionary 
    embeddings_dictionary[word] = representation
    
# Close the file
glove_file.close()

# Initialize the embedding_matrix
embeddings_matrix = np.zeros((vocab_size, embedding_dimension))

# Iterate through the tokenizer words list
for word, index in tokenizer.word_index.items():
    # Get the word representation
    embedding_vector = embeddings_dictionary.get(word)
    # Update the word representation if it exist in our dictionary
    if embedding_vector is not None:
        embeddings_matrix[index] = embedding_vector


# ### Define the model

# In[ ]:


import torch.nn

def create_emb_layer(weights_matrix, non_trainable=False):
    num_embeddings, embedding_dim = weights_matrix.size()
    emb_layer = nn.Embedding(num_embeddings, embedding_dim)
    emb_layer.load_state_dict({'weight': weights_matrix})
    if non_trainable:
        emb_layer.weight.requires_grad = False

    return emb_layer, num_embeddings, embedding_dim

