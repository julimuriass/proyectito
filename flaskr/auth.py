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