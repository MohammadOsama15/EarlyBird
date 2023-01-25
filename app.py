import flask

app = flask.Flask(__name__)

@app.route('/')
def search():
    return 'Search Page'

if __name__ =='__main__':
    app.run()