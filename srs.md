# 1. Introduction

## 1.1 Purpose
This document describes the implementation details and objectives of our upcoming Twitter sentiment analysis web app, EarlyBird. 

## 1.2 Intended Audience*
The audience of this document is students and instructors in CSC 4351/4352, to communicate our building process and inspire others in developing their own applications.

## 1.3 Intended Use
This document will serve as a guideline to create and prioritize tasks while building our project. Our roadmap document will go into further detail, listing specific tasks and describing a projected timeline. This spec will be used only loosely to measure the success of our project; in the sense of general categories of goals being achieved rather than hitting every potential feature described here.


## 1.4 Scope
Twitter is one of the largest datasets in the world containing sentiments of users on a variety of topics, such as politics, consumer products, social issues, relationships, current events, entertainment and more. The sentiment is defined as having positive, negative or neutral feelings toward something/a topic. Anyone who wants to understand the sentiment of an individual, group or subgroup on a topic and can gain valuable insight from the Twitter dataset. Aggregation and analysis of this data can be automated by computers, using natural language processing to parse the data into an interpretable format and machine learning to measure sentiments and trends. Our application will use these techniques and provide a front end to visualize the results and make the analysis available in a format suitable for data science exploration.


## 1.5 Definitions and Acronyms
The remainder of this document will use the following conventions:
* “EarlyBird” will refer to our application in its entirety.
* “User” will refer to a user of EarlyBird.
* “Tweeter” will refer to a user of Twitter (i.e. a User is  performing sentiment analysis on that Tweeter’s Twitter account).

In addition:
* “ML” refers to any machine learning technique.
* “NLP” refers to natural language processing.
* “TF” refers to the TensorFlow deep learning framework.
* “GloVe” is a library of pre-trained word vectors we will use to inform our neural network of tweet semantics.

# 2. Overall Description

## 2.1 User Needs
EarlyBird attempts to solve the following problems:
* Users interested in launching a product/service need to assess the sentiment of their potential customers/audience.
* Organizations already providing a product/service may want to use Twitter as an avenue to understand audience sentiment.
* Twitter provides a large quantity of sentiment data, but in an unstructured and disparate format.
EarlyBird will solve the problems above by performing sentiment analysis on tweets by a Tweeter, or tweets by many Tweeters on a topic, and output the results in an accessible format.


## 2.2 Assumptions and Dependencies
Our app makes the following assumptions:
* For analysis of an individual account, the Tweeter is human (not a bot).
* For analysis of many Tweeters tweeting about a topic, there are sufficient tweets to perform statistical analysis.

Other significant dependencies: 
* We will use TF or PyTorch to create our neural network and train our machine learning model for predicting whether a tweet contains positive, negative or neutral sentiment.
* We will train our model on the Sentiment140 dataset (1.6 million tweets annotated with sentiment values from 0 - 4; 0 = negative, 2 = neutral, 4 = positive).
* We will use Python data science libraries to perform remaining analysis tasks and return raw data exports.
* We will use the Twitter API to fetch tweets corresponding to the topic/user searched.