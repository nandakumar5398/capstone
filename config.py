import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enabling debug mode.
DEBUG = True

# Connecting to the database

#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/capstone'
SQLALCHEMY_DATABASE_URI = 'postgres://pzlwtqgzcuohsk:d76f3f9f10bc72ad02bf6147b1a52eeb54ba920994ede3419681875a1dcc8334@ec2-18-209-187-54.compute-1.amazonaws.com:5432/dchkpjunb9i0v3'
SQLALCHEMY_TRACK_MODIFICATIONS = False