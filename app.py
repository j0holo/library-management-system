import os
from flask import Flask, render_template, request
from flask import redirect, url_for, flash
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
    return render_template('admin_publisher.html',
                           publishers=publishers)

@app.route('/admin/publisher/update/<int:publisher_id>',
           methods=['GET', 'POST'])
def update_publisher(publisher_id):
    if request.method == 'POST':
        publisher = Publisher.update_selected(
            publisher_id,
            request.form['name'],
            request.form['city']
        )
        if publisher:
            return redirect(url_for('view_publishers'))
        elif publisher is None:
            flash("Publisher %d does not exist" % publisher_id)
            return redirect(url_for('view_publishers'))
        else:
            flash("Input should be less than 266 characters")
            return render_template('update_publisher.html',
                                   publisher_id=publisher_id)
    else:
        try:
            publisher = Publisher.get(Publisher.id == publisher_id)
        except Publisher.DoesNotExist:
            flash("Publisher %d does not exist" % publisher_id)
            return redirect(url_for('view_publishers'))
        return render_template('update_publisher.html',
                               publisher_id=publisher_id)


@app.route('/admin/publisher/add', methods=['GET', 'POST'])
def add_new_publisher():
    if request.method == 'POST':
        if request.form['name'] and request.form['city']:
            Publisher.add_publisher(request.form['name'],
                                    request.form['city'])
            return redirect(url_for('view_publishers'))

        else:
            flash("Both fields are required")
    return render_template('add_publisher.html')

@app.route('/admin/publisher/delete/<int:publisher_id>')
def delete_publisher(publisher_id):
    if Publisher.delete_selected(publisher_id):
        flash("Publisher %d has been deleted" % publisher_id)
        return redirect(url_for('view_publishers'))

    flash("Publisher %d does not exist" % publisher_id)
    return redirect(url_for('view_publishers'))


if __name__ == '__main__':
    db.init(host=os.getenv('DB_HOST', 'localhost'),
            user='development',
            password='devpassword',
            database='devdatabase',
            charset='utf8')
    app.run()
