import os
from flask import Flask, render_template
from models import *


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='development key',
    # USER='development',
    # PASSWORD='devpassword',
    # DATABASE='devdatabase',
    # CHARSET='utf8',
    # HOST=os.getenv('DB_HOST', 'localhost'),
    DEBUG=True
))


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.route('/admin/publisher')
def view_publishers():
    publishers = Publisher.select_all()
    if publishers is None:
        return "No publishers here"
    return render_template('admin_publisher.html',
                           publishers=publishers)


if __name__ == '__main__':
    db.init(host=os.getenv('DB_HOST', 'localhost'),
            user='development',
            password='devpassword',
            database='devdatabase',
            charset='utf8')
    app.run()
