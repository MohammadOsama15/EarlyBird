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

# 3. System Features and Requirements

## 3.1 Functional requirements

### 3.1.1 Functional requirement 1 - search page

Description: As a User, I can choose between one of two modes - performing analysis on an individual Tweeter, or on many tweets relating to a topic.

Acceptance criteria:
* The landing page will have two buttons, one directing to each mode.
* For the “individual account” mode, the subsequent page will have a form and a submit button to enter a Twitter handle.
* For the “topic” mode, the subsequent page will have a form and a submit button to query the Twitter API for a topic/string.
* There will be an “information” hover button explaining the difference between the two modes for new Users.


### 3.1.2 Functional requirement 2 - information page

Description: As a User, I can learn more information about what a Twitter sentiment analyzer is.

Acceptance criteria:
* Users can click on the information symbol on the top right of the main page which will take them to the information page.
* Users will be able to see information regarding what a Twitter sentiment analyzer
* Users will be able to see information about who has made this app and how to contact them.
A back button should be present to redirect the user back to the main page. 


### 3.1.3 Functional requirement 3 - Viewing a Tweeter’s most-tweeted-about topics

Description: Using the “individual account” mode, Users can search for a Tweeter and view their most tweeted-about topics.

Acceptance criteria:
* When the User starts typing a username in the search box, a dropdown list of suggested Tweeter handles (starting with the string entered) should appear.
* After hitting the submit button, a page displaying the topics most frequently tweeted about by the Tweeter will be displayed.
* The topics will be displayed in a word cloud shaped like the Twitter logo.
* Words in the word cloud will be larger the more the Tweeter tweets about them.


### 3.1.4 Functional requirement 4 - analyzing sentiment on topics an Account tweets about

Description: After navigating to the word cloud of topics, a User can click on any word shown to understand the Tweeter’s sentiment on that topic.

Acceptance criteria:

* The clicked-on topic will redirect the User to a page displaying lists of the Tweeter’s posts on that topic
* The default view will be of two lists of tweets, positive and negative. The lists will be sorted from strongest to weakest sentiment; i.e. the negative list will have the most negative tweets at the top and weakly negative at the bottom, and similarly for the positive list.
* A dropdown menu or other selector will be implemented to allow Users to sort the tweets by different parameters besides sentiment strength (e.g. date).
* A back button should be present to redirect the User back to the main page. 

### 3.1.5 Functional requirement 5 - viewing results regarding a certain topic
Description: As a User, I can search for a topic and understand the sentiment of Tweeters across Twitter.

Acceptance criteria:
* After searching the topic, users will be redirected to a page displaying the sentiment of Twitter users regarding that topic. 
* Users will be able to slide through a bar on the bottom that would allow them to filter people’s sentiments regarding that topic. 
* UI elements will be updated dynamically according to the sentiment score the topic receives. 
* Implement a slider filter results based on sentiment score.
* When a user searches certain topics they will be suggested similar topics people have searched on Twitter.
* A back button should be present to redirect the user back to the main page. 

### 3.1.6 Functional requirement 6 - export analysis of individual accounts for offline use
Description: As a User, I can download the sentiment analysis performed by EarlyBird on a Tweeter to use in my own data experiments.

Acceptance criteria:
* Data is accessible in CSV, JSON or other widely used formats.
* All data and statistics used to generate data views included in the UI will be exported, including tweet content.
* Users can set start and end dates for tweets considered in the export.
* Users can choose between their preferred export formats.

### 3.1.7 Functional requirement 7 - export analysis of topics for offline use
Description: As a User, I can download the sentiment analysis performed by EarlyBird on a topic to use in my own data experiments.

Acceptance criteria:
* Data is accessible in CSV, JSON or other widely used formats.
* All data and statistics used to generate data views included in the UI will be exported, including tweet content.
* Users can set start and end dates for tweets considered in the export.
* Users can choose between their preferred export formats.

### 3.1.8 Functional requirement 8 - revisit page
Description: As a User, I will be able to see my query history in both modes of the app.

Acceptance criteria:
* A cookie will be used as a token for stored query parameters associated with each user’s session.
* On a subsequent visit, the cookie will be used as a token to fetch information from the database.
* Query parameters submitted previously will be displayed as a list associated with the search input box (similar to Google suggestions).
* Cookies will expire after a fixed amount of time; users will have the option to opt out and not have anything cached for his or her session

## 3.2 External Interface Requirements
See our design mockups in the `mockups` folder for visual specifications.

## 3.3 System Requirements*
Users of our application need a computer with access to the internet, and a modern web browser that can render JavaScript.

## 3.4 Nonfunctional Requirements
1. On a 10 Mbps connection, each server request should complete within 5 seconds. A server is busy and a message will be displayed if too many queries are submitted simultaneously.
2. The UI should be simple to navigate and free of clutter. This means minimizing the number of input boxes, submit buttons, dropdown menus, and so on. Important page elements should be sufficiently visible to the user.
3. The UI should follow a design theme such that all elements blend well together.
4. Sentiment classifier should be sufficiently accurate (we set our initial goal to be 60% accurate when compared against training dataset)