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
    # POST with error -> show form again with error message.
   
@bp.route('/login', methods=('GET', 'POST'))
def login():
    pass
   # if request.method == 'POST'