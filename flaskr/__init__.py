import os # Lets you interact with the operating system (Used to build file paths and create directories).
from flask import Flask

def create_app(test_config=None): 
    ''' test_config=None -> 
            The fn accepts one argument called test_config
            if you don't pass anything test_config will be None
    '''

    app = Flask(__name__, instance_relative_config=True)
    '''instance_relative_config=True tells the app that configuration 
    files are relative to the instance folder. The instance folder is 
    located outside the flaskr package and can hold local data that
    shouldn’t be committed to version control, such as configuration 
    secrets and the database file.'''



    '''app.config is just a dictionary-like object:
                app.config['SECRET_KEY']
                app.config['DATABASE']'''
    
    app.config.from_mapping(
        SECRET_KEY='dev', # Used to sign cookies, protect sessions, prevent tampering.
        # 'dev' is a placeholder, this value is expected to be overridden later.

        # This builds the path to your database file.
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), # Keeps database out of the source code.
    )


    # Switching behavior for tests vs normal runs.

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True) # Actually overrides 'dev' if the file exists.
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        ''' Flask skips loading config.py
            Uses only test settings'''

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    '''ensures that app.instance_path exists. 
    Flask doesn’t create the instance folder automatically, 
    but it needs to be created because your project will 
    create the SQLite database file there.'''

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    return app
