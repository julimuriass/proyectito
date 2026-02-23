import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

''' Flash: Used to show temporary messages to the user. Example: flash("Login successful!")
   Redirect: sends the user to another URL.
   session: used to store data between requests (per user). 
   url_for: builds URLs dynamically.
'''

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db # This imports your database connection function.

# This creates a Blueprint. 'auth' is the bp name, __name__ tells Flask where this module lives, url_prefix='/aux' means that everyroute inside this blueprint will start with /auth.
bp = Blueprint('auth', __name__, url_prefix='/auth')


# @bp.route associates the URL /register with the register view fn. When Flask receives a req to /auth/register, it will call the register view and use the ret value as the rt.
@bp.route('/register', methods=('GET', "POST")) # GET -> Show the form. POST -> Process the form.
def register():
    if request.method == 'POST': # request.methos tells you how the page was accessed. GET -> user just opened the page. POST -> user submitted the form.
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required :/'
        elif not password:
            error = 'Password is required :/'

        if error is None:
            try: # Try to insert the user.
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",  # The ? are placeholders (2 prevent SQL injection) -> They mean: SQLite, I will give you the real values separately (and then woy pass them like in the next line.)
                    (username, generate_password_hash(password))
                )
                db.commit() # This saves the changes permanently.
            except db.IntegrityError: # Trying to insert the same username twice triggers it. (If ur username column is defined as username TEXT UNIQUE, which is).
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))  # POST successful -> redirect to login.
        
        flash(error)
            
    return render_template('auth/register.html') # This always runs when the request is GET or there was an error in POST.
    # GET request -> just shows the form.
    # POST with error -> shows form again with error message.
   
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username)
        ).fetchone() # fetchone() returns the next single row from the result of a query. If there are no more rows left it returns None.

        if user is None:
            error = 'Incorrect username :p'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password >:|'
        
        if error is None:
            session.clear() # session is a dict that stores data across requests.
            session['user_id'] = user['id'] # When validation succeeds, the user's id is stored in a new session.
            return redirect(url_for('index'))
    
    return render_template('auth/login.html')


'''Now that the user’s id is stored in the session, it will be available on subsequent requests. 
At the beginning of each request, if a user is logged in their information should be loaded and made available to other views.'''

@bp.before_app_request
def load_logged_in_user(): # Checks if a user is stored in the session and gets that user's data from the db, storing it on g.user, which lasts for the length of the request.
    user_id = session.get('user_id')

    if user_id is None: # If there is no user id, or if the id doesn't exist, g.user will be None.
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear() # Removes the user id from the session.
    return redirect(url_for('index'))


# Decorator to protect routes.
def login_required(view): # view is the view function that we want to protect.
    @functools.wraps(view) # This is another decorator. It preserves the original fn's name and metadata

    # This fn replaces the origianl view.
    def wrapped_view(**kwargs): # **kwargs allows it to accept any keyboard arguments the route might receive.
        if g.user is None:
            return redirect(url_for('auth.login')) 

        return view(**kwargs) # Call the original view fn, pass along any arguments it needs.
    
    return wrapped_view # Returns the fn itself (it doesn't run it because it's not return wrapped_view())