from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

# INDEX.

@bp.route('/') # Since there's no methods=, flask defaults to methods = ['GET'].
def index():
    db = get_db()
    posts = db.execute (
        'SELECT p.id, title, body, created, author_id, username'
        'FROM post p JOIN user u ON p.author_id = u.id'
        'ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts) # posts=posts. Left side -> var name in the template, right side -> python var. It means that inside index.html, there will be a ver called posts
    # "Render the template blog/index.html, pass it some data, return the generated HTML to the user."
    # Returns a string of HTML. ("Send this HTML back as the response")

# CREATE.

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create(): # Python secretly does this: create = login_required(create). Which then, becomes create = wrapped_view (auth.py).
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required :/'

        if not body:
            error = 'Body is required :/'

        if error is not None:
            flash(error)

        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)',
                'VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
        
    return render_template('blog/create.html')

