import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture # A piece of setup code that prepares something tests need.
def app():
    db_fd, dp_path = tempfile.mkstemp() # This uses the Python module tempfile to create a temporary file. The fn returns 2 things -> (file_descriptor, file_path)
    # db_fd -> file descriptor (low-level handle to the file (a low-level number representing the open file))

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })