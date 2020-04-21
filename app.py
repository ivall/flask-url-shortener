from flask import Flask, render_template, redirect, url_for, jsonify, abort, request
from flask_mysqldb import MySQL, MySQLdb
import string
import random
import validators

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)


def random_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/short', methods=['POST'])
def short():
    url = request.form['longurl']
    if validators.url(url):
        shorturl = random_generator()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO links (originalurl, shorturl) VALUES (%s,%s)", (url, shorturl,))
        mysql.connection.commit()
        return jsonify({'shorturl': shorturl})
    return abort(400)


@app.route('/<link>', methods=['GET'])
def link(link):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM links WHERE shorturl=%s", (link,))
    fetchdata = cur.fetchone()
    if fetchdata is None:
        return redirect(url_for('index'))
    cur.close()
    originalurl = fetchdata['originalurl']
    return redirect(originalurl)


if __name__ == '__main__':
    app.run()
