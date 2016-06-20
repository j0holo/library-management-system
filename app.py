import os
from flask import Flask, render_template, request, redirect, url_for
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
        return render_template('admin_publisher.html',
                               publishers=publishers)
    return render_template('admin_publisher.html',
                           publishers=publishers)

@app.route('/admin/publisher/<int:publisher_id>',
           methods=['GET', 'POST'])
def update_publisher(publisher_id):
    error = None
    if request.method == 'POST':
        if Publisher.update_selected(publisher_id,
                                     request.form['name'],
                                     request.form['city']):
            return redirect(url_for('view_publishers'))
        else:
            error = "Input should be less than 266 characters"

    return render_template('update_publisher.html', error=error,
                           publisher_id=publisher_id)


@app.route('/admin/publisher/add', methods=['GET', 'POST'])
def add_new_publisher():
    error = None
    if request.method == 'POST':
        if request.form['name'] and request.form['city']:
            Publisher.add_publisher(request.form['name'],
                                    request.form['city'])
            return redirect(url_for('view_publishers'))

        else:
            error = "Both fields are required"
    return render_template('add_publisher.html', error=error)


if __name__ == '__main__':
    db.init(host=os.getenv('DB_HOST', 'localhost'),
            user='development',
            password='devpassword',
            database='devdatabase',
            charset='utf8')
    app.run()
