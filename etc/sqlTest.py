import flask
from flask_mysqldb import MySQL

app = flask.Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "embed your password in .env file"
app.config['MYSQL_DB'] = 'earlybird'
with app.app_context():
    # create a connection with cursor.
    cursor = mysql.connection.cursor()
    print(cursor)

    # Test data to check the database connection. Works!
    username = "Mohammad"
    email = "blahblah@blah.com"
    password = "moreblahblah"
    create_time = "2023-02-01 12:59:59"
    # database columns are denoted by %s in exact order as designed.
    cursor.execute('INSERT INTO user VALUES(%s,%s,%s,%s)',
                   (username, email, password, create_time))

    # Saving the Actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()


@app.route('/')
def index():
    return "hello world"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
