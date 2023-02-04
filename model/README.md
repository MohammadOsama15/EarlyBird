# README
This contains a short discussion on the research that went into choosing our model training methodology.

## General approach
The machine learning aspect of this project is an NLP (natural language processing) problem. We need to find a way to represent the semantic meaning of words, and extrapolate the sentiment of a tweet based on the words in it. Deep learning is well-suited to NLP, and commonly used for sentiment analysis. We will train a model for predicting tweet sentiment, then call the trained model from our application to analyze individual tweets and also find average "net" sentiment scores for Twitter accounts. 

The rest of this document details our process for selecting particular tools, partly from trial and error but mainly from researching various examples and online documentation (which are cited at the end of `tf_train.ipynb`).

## Tooling
### TensorFlow vs PyTorch
Generally, TF vs PyTorch is seen as a matter of opinion. We tried both, and ultimately settled on TensorFlow for the following reasons:
* PyTorch is very 'pythonic' and allows for detailed, object-oriented definition of training layers and preprocessing functions. However, this level of detail is not necessary for a simple problem such as basic sentiment analysis, and we found ourselves spending more time dealing with conflicting Python packages than coding and training our model.
* TensorFlow provides a complete one-stop shop for NLP preprocessing and tokenization, as well as model training. PyTorch offers many of these capabilities as well, but requires more external imports.
* Generally speaking, we see PyTorch's appeal for research as it is easier to implement custom code, such as a novel loss function. However, this project is not such a project and TensorFlow's higher level of abstraction and self-sufficiency made it the best choice.

### Word embeddings
Word embeddings are a simple way to improve NLP model prediction accuracy. We will use GLoVe word embeddings in our neural network layers to pass refined tweets semantic into our model. You can download the embeddings [here.](https://nlp.stanford.edu/projects/glove/)

### Dataset
The Sentiment140 dataset provides a large volume of tweets prelabeled with sentiment scores, which we split into train and test sets. You can find it [here.](http://help.sentiment140.com/for-students)

