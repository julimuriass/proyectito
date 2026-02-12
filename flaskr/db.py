import sqlite3 # Python comes with a built-in support for SQLite in the sqlite3 module.
from datetime import datetime

import click # Click is used to create command-line commands.
from flask import current_app, g
''' g: is a special object that is unique for each request. It's used to store data
that might be accessed by multiple fn during the request. The connection is stored and reused
instead of creating a new connection id get_db is called a second time in the same request.

current_app: a special object that points to the Flask application handling the request.
Since I used an application factory, there's no app object when writing the rest of
my code. get_db will be called when the app has been created and is handling a request, so 
current_app can be used.'''

def get_db():
    if 'db' not in g: # Checks whether a db connection is already stored in g.
        # So if g.db doesn't exist yet, create it.
        g.db = sqlite3.connect( # Establishes a connection to the file pointed by the DATABASE configuration key. This file doesn't exist yer, and won't until you initialize the db later.
            current_app.config['DATABASE'], # Gets the path to the database file from Flask config.
            # This was set earlier in create_app() like: DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'). So it's connecting to that file.
            detect_types=sqlite3.PARSE_DECLTYPES # Automatically convert database types (like timestamps) into proper Python types (like datetime objects).Without this, everything would come back as strings.
        )

        g.db.row_factory = sqlite3.Row # tells the connection to return rows that behave like dicts. This allows accessing the columns by name.

    return g.db # Returns the database connection (either newly created or already existing).

def close_db(e=None): # e=None allows Flask to pass an error object if something failed.
    db = g.pop('db', None) # Removes 'db' from g, returns its value (or None of it didn't exist).

    if db is not None: # Checks if a connection was found.
        db.close()

def init_db(): # It builds your database structure from scratch.
    db = get_db() # Opens the connection to the SQLite db, and stores it in g.
    # So now db is my active db connection.

    with current_app.open_resource('schema.sql') as f: 
        # current_app refers to the active Flask application.
        # open_resource('schema.sql') tells Flask to open the file called 'schema.sql' inside the application folder.
        db.executescript(f.read().decode('utf8'))
        # executescript() runs MULTIPLE SQL statements at once. It executes the entire SQL file in one go.
        # f.read() reads the entire contents of schema.sql, but it returns bytes, not a string.

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


# The call to sqlite3.register_converter() tells Python how to interpret timestamp values in the database. We convert the value to a datetime.datetime.
sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)
