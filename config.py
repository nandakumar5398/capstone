import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enabling debug mode.
DEBUG = True

# Connecting to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/capstone'
SQLALCHEMY_TRACK_MODIFICATIONS = False