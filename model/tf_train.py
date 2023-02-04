#!/usr/bin/env python
# coding: utf-8

# # Training our model
# This notebook trains a model that takes a tweet as input and outputs a score between 0 and 1. 0 is negative sentiment, 0.5 is neutral sentiment, and 1 is positive sentiment.
# 
# We use TensorFlow to train our model; and Scikit-Learn, Numpy and Pandas for preparing training data. We use GLoVe word embeddings in our neural network. Our train and test data are from the Sentiment140 dataset.
# 
# The training data folder in Github is empty as we are having issues with Git LFS. We plan to resolve this later.

# In[2]:


# Regular expressions
import re

# Data and visualization 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Calculations
import numpy as np

# Machine Learning
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Deep Learning
import tensorflow as tf
from tensorflow.keras.layers import Embedding, LSTM
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# In[3]:


df = pd.read_csv("data/train.csv", 
                      encoding="latin", 
                      header=None, 
                      names=["target","id","date","query","username","content"]
                     )


# In[4]:


df.head()


# In[6]:


print(f"Missing values: \n\n{df.isna().sum()}")


# In[7]:


negative_samples = df[df["target"]==0]
print(f"Number of negative samples : {len(negative_samples)}\n")
negative_samples.head(5)


# In[9]:


neutral_samples = df[df["target"]==2]
print(f"Number of neutral samples : {len(neutral_samples)}\n\n")
neutral_samples.head(5)


# In[10]:


positive_samples = df[df["target"]==4]
print(f"Number of positive samples {len(positive_samples)}\n\n")
positive_samples.head(5)


# In[11]:


data = [len(negative_samples), len(neutral_samples), len(positive_samples)]
labels = ["Negative","Neutral","Positive"]


# In[12]:


colors = sns.color_palette("pastel")


# In[13]:


plt.figure(figsize=(6,6))
plt.title("Target distribution")
plt.pie(data, labels=labels, colors=colors, autopct="%.0f%%")
plt.show()


# In[15]:


df.drop(["id","date","query","username"],axis=1, inplace=True)


# In[17]:


df.head(5)


# In[19]:


df.target = df.target.replace({4: 1})


# In[20]:


df[df["target"]==1].head()


# ## Preparing training data

# In[21]:


regex_mentions = r"@[A-Za-z0-9_]+" # Remove mentions
regex_links = r"https?://[A-Za-z0-9./]+" # Remove links
regex_special = r"[^A-Za-z0-9]+" # Remove some special characters


# In[23]:


# Apply the above
df.content = df.content.apply(lambda x: re.sub(regex_mentions, " ", str(x).strip()))
df.content = df.content.apply(lambda x: re.sub(regex_links, " ", str(x).strip()))
df.content = df.content.apply(lambda x: re.sub(regex_special, " ", str(x).strip()))


# In[25]:


df.head(10) # Results


# In[27]:


print(f"Null values: \n\n{df.isna().sum()}")


# In[29]:


train, test = train_test_split(df, test_size=0.1, random_state=44) # Split data into train and test set


# In[30]:


print(f"Training set length: {len(train)/1e6}M examples")
print(f"Test set length: {len(test)/1e6}M examples")


# In[31]:


'''
    Here we tokenize our data, i.e. split it into 'meaningful' parts. The Keras tokenizer represents each meaningful word as a vector of integers.
'''
tokenizer = Tokenizer()
# Updates the internal vocabulary based on our tweet contents
tokenizer.fit_on_texts(train.content)
# Setup the vocabular size based on the tokenizer results
vocab_size = len(tokenizer.word_index)+1


# In[32]:


print(f"Word index length: {len(tokenizer.word_index)}")
print(f"Some words: {list(tokenizer.word_index.keys())[0:10]}")


# In[34]:


# Intialize the max length to the first tweet length
max_length = len(df["content"][0].split())

# Loop through the tweets
for tweet in df["content"]: 
    # Get each tweet's length
    length = len(tweet.split())
    # Update the max length if greater
    if length > max_length: 
        max_length = length

print(f"Maximum token length: {max_length}")


# In[35]:


sequences_train = tokenizer.texts_to_sequences(train.content) # Train data
sequences_test = tokenizer.texts_to_sequences(test.content) # Test data


# In[36]:


# Pad the training and test sequences to the same length after the sequence
X_train = pad_sequences(sequences_train, maxlen=max_length, padding="post")
X_test = pad_sequences(sequences_test, maxlen=max_length, padding="post")

# Setup the training and test target values (sentiment scores)
y_train = train.target.values
y_test = test.target.values

print(f"Training test shape : {X_train.shape}")


# In[49]:


embeddings_dictionary = dict()
embedding_dimension = 100
glove_file = open("data/glove.6B.50d.txt")


# In[47]:


print()


# In[50]:


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


# # Citations
# We are grateful for the following source:
# * https://www.kaggle.com/code/ibrahimserouis99/twitter-sentiment-analysis/notebook
# * https://www.kaggle.com/datasets/kazanova/sentiment140
# * https://www.tensorflow.org/api_docs/

# 
