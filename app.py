import flask
from flask import send_file


app = flask.Flask(__name__)
@app.route('/')
def welcome():
    return send_file('./templates/welcome.html')

@app.route('/login')
def login():
    return send_file("./templates/login.html")

@app.route('/signup')
def signup():
    return send_file("./templates/signup.html")

@app.route('/logout')
def logout():
    return send_file("./templates/logout.html")
    
@app.route('/search')
def search():
    return send_file("./templates/search.html")

@app.route('/information')
def information():
    return send_file("./templates/info.html")

@app.route('/userTopic')
def userTopic():
    return send_file("./templates/userTopic.html")

@app.route('/userSentiment')
def userSentiment():
    return send_file("./templates/userSentiment.html")

@app.route('/topicSentiment')
def topicSentiment():
    return send_file("./templates/topicSentiment.html")

if __name__ =='__main__':
    app.run()