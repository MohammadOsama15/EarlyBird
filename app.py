import flask
from flask import render_template


app = flask.Flask(__name__)
@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/logout')
def logout():
    return render_template("logout.html")
    
@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/information')
def information():
    return render_template("information.html")

@app.route('/userTopic')
def userTopic():
    return render_template("userTopic.html")

@app.route('/userSentiment')
def userSentiment():
    return render_template("userSentiment.html")

@app.route('/topicSentiment')
def topicSentiment():
    return render_template("topicSentiment.html")

if __name__ =='__main__':
    app.run()