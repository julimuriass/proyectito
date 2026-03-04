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

        # Not null means the value cannot be nill, but is can still be an empty string, that's why I don't check for body.

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


# Both the update and delete views will need to fetch a post by id and check if the author matches the logged in user.
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, uthor_id, username'
        'FROM post p JOIN user u ON p.author_id = u.id'
        'WHERE p.id = ?',
        (id,)
    ).fetchone() # It’s fetching one specific post by its ID.

    if post is None:
        abort(404, f"Post if {id} doesn't exist.") # abort() will raise a special exception that returns an HTTP status code. 

    if check_author and post['author_id'] != g.user['id']:
        abort(403) # 403 means "Forbidden".
    
    return post

# UPDATE.

# ('/<int:id>/update' is a URL var. It means: 'Expect a number in this part of the URL, and store is in a var called id.
# int: is a converter.
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        # It updates both columns every time. But you can leave one unchanged — it will just re-save the same value.
        title = request.form['title']
        body = request.form['post']
        error = None

        if not title:
            error = 'Title is required.'
        
        if error is not None: 
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                'WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
        
    return render_template('blog/update.html', post=post)

