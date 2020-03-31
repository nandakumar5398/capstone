# imports

import json
from flask import Flask, jsonify, request, abort, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from jose import jwt
from functools import wraps
from urllib.request import urlopen


# App configuration

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

AUTH0_DOMAIN = 'cshop.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'
Client_ID = '54SRzrOYZo9QeLF7oP4dPWrLnijm6dID'


# models

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
            }


class Actors(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
            }

db.create_all()


# App authentication

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# Auth Header


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        abort(403)
    parts = auth.split(' ')
    if parts[0].lower() != 'bearer':
        print('bearer not found')
        abort(403)
    elif len(parts) == 1:
        print('invalid header')
        abort(423)
    elif len(parts) > 2:
        abort(423)
        print('invalid header')
    token = parts[1]
    return token

# checking for permissions


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        print('error at check')
        abort(401)
    if permission not in payload['permissions']:
        print('error at check 2')
        abort(401)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen('https://cshop.auth0.com/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except:
            return 'Error at rsa_key'


def requires_auth(permission=''):
    def requires_auth_role(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_role


# Endpoints

@app.route('/')
def start_up():
    return jsonify({
        "ForAuthenticating": "https://capstone-master.herokuapp.com/login",
        "ForLogout": "https://cshop.auth0.com/v2/logout",
        "Action": "Result",
        "/actors (GET)": "Gives all actors present",
        "/movies (GET)": "Gives all movies present",
        "/actors/<actor_id> (DELELTE)": "Deletes actor with the id",
        "/movies/<movie_id> (DELELTE)": "Deletes movie with the id",
        "/actors/<actor_id> (PATCH)": "Edits actor with the id",
        "/movies/<movie_id> (PATCH)": "Edits movie with the id",
        "/movies (POST)": "Creates new movie",
        "/actors (POST)": "Cretes new actors"
        })

@app.route('/test')
def for_test():
    return jsonify({
        "Result": "Passed"
    })

@app.route('/login')
def login():
    link = 'https://cshop.auth0.com/authorize?'
    link = link + 'audience=capstone&response_type=token&'
    link = link + 'client_id=54SRzrOYZo9QeLF7oP4dPWrLnijm6dID&'
    link = link + 'redirect_uri=https://capstone-master.herokuapp.com/'
    return redirect(link)


@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(payload):
    data = Actors.query.all()
    fromatted_actors = [Actors.format() for Actors in data]
    return jsonify({
        "Actors": fromatted_actors
        })


@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(payload):
    data = Movies.query.all()
    formatted_movies = [Movies.format() for Movies in data]
    return jsonify({
        'Movies': formatted_movies
    })


@app.route('/actors/<actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(payload, actor_id):
    temp = Actors.query.filter_by(id=actor_id).all()
    if temp == []:
        abort(422)
    else:
        Actors.query.filter_by(id=actor_id).delete()
        db.session.commit()
        return jsonify({
            'Status': True,
            'Message': 'Your request is executed successfully'
            })


@app.route('/movies/<movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(payload, movie_id):
    temp = Movies.query.filter_by(id=movie_id).all()
    if temp == []:
        abort(422)
        return jsonify({
            'status': False,
            'Message': 'There is no actor/movie with provided id'
        })
    else:
        Movies.query.filter_by(id=movie_id).delete()
        db.session.commit()
        return jsonify({
            'Status': True,
            'Message': 'Your request is executed successfully'
            })


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actors(payload):
    js = request.get_json()
    print(js["age"])
    if js["name"] == "" or js["age"] == 0 or js["gender"] == "":
        abort(400)
    else:
        data = Actors(
            name=js["name"],
            age=js["age"],
            gender=js["gender"]
        )
        print(data)
        db.session.add(data)
        db.session.commit()
    return jsonify({
        'Status': True,
        'Message': 'Your request is executed successfully'
        })


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movies(payload):
    js = request.get_json()
    if js["title"] == "" or js["release_date"] == "":
        abort(400)
    else:
        data = Movies(
            title=js["title"],
            release_date=js["release_date"]
        )
        print(data)
        db.session.add(data)
        db.session.commit()
    return jsonify({
        'Status': True,
        'Message': 'Your request is executed successfully'
        })


@app.route('/actors/<actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actors(payload, actor_id):
    temp = Actors.query.filter_by(id=actor_id).all()
    if temp == []:
        abort(422)
    else:
        js = request.get_json()
        print(js["age"])
        if js["name"] == "" or js["age"] == 0 or js["gender"] == "":
            abort(400)
        else:
            updated_name = js["name"],
            updated_age = js["age"],
            updated_gender = js["gender"]
            actor = Actors.query.filter_by(id=actor_id).first()
            actor.name = updated_name
            actor.age = updated_age
            actor.gender = updated_gender
            db.session.commit()
            return jsonify({
                'Status': True,
                'Message': 'Your request is executed successfully'
                })


@app.route('/movies/<movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movies(payload, movie_id):
    temp = Movies.query.filter_by(id=movie_id).all()
    if temp == []:
        abort(422)
    else:
        js = request.get_json()
        if js["title"] == "" or js["release_date"] == "":
            abort(400)
        else:
            updated_title = js["title"],
            updated_release_date = js["release_date"]
            movie = Movies.query.filter_by(id=movie_id).first()
            movie.title = updated_title
            movie.release_date = updated_release_date
            db.session.commit()
            return jsonify({
                'Status': True,
                'Message': 'Your request is executed successfully'
                })


# error handlers

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "There is no actor/movie with provided id"
        }), 422


@app.errorhandler(401)
def Unauthorized(error):
    return jsonify({
                    "success": False,
                    "error": 401,
                    "message": "Unauthorized"
                    }), 401


@app.errorhandler(404)
def resnotfound(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(403)
def authnotfound(error):
    return jsonify({
                    "success": False,
                    "error": 403,
                    "message": "Authorization not found"
                    }), 403


@app.errorhandler(423)
def invalidheader(error):
    return jsonify({
                    "success": False,
                    "error": 423,
                    "message": "Invalid header"
                    }), 423


@app.errorhandler(400)
def fields(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "Please make sure all data is given"
                    }), 400


@app.errorhandler(405)
def fields(error):
    return jsonify({
                    "success": False,
                    "error": 405,
                    "message": "Method Not Allowed"
                    }), 405


if __name__ == '__main__':
    app.run(debug=True)
