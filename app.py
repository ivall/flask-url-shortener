from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL, MySQLdb
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, validators
import string
import random

app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL(app)

def random_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


class UrlForm(Form):
    url = StringField('url', [validators.DataRequired(), validators.Length(min=6, max=255), validators.url()])
    recaptcha = RecaptchaField()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = UrlForm()
    if request.method == 'GET':
        return render_template('index.html', form=form)
    else:
        if form.validate_on_submit():
            url = form.url.data
            shorturl = random_generator()
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO links (originalurl, shorturl) VALUES (%s,%s)", (url, shorturl,))
            mysql.connection.commit()
            session['mojurl'] = shorturl
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))


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
