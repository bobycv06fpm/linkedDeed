from __future__ import print_function # In python 2.
import sys
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__.split('.')[0])   # create the application instance


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect('stuffToPlot.db')
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    init_db()
    db = get_db()
    cur = db.execute('select title, description from stuffToPlot order by id desc')
    entries = cur.fetchall()
    for job in entries:
        print(dir(job), file=sys.stderr)
        print(type(job), file=sys.stderr)
    return render_template('jobs.html', entries=entries)

"""
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))"""


@app.route('/index', methods=['POST'])
def login():
    url = request.form['url']
    em = request.form['email']
    pwd = request.form['password']
    what = request.form['what']
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)