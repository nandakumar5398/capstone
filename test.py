import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors

class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'password','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path) 

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.actor = {
            "name":"test_actor",
            "age":"32",
            "gender":"M"
        }

        self.movie = {
            "name":"test_movie",
            "release_date":"2020-02-02"
        }

        self.header_director = {"Authorization":"Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5EZEJOVFJFTlRRMlJqRkVNRFV4UlVZMlFqVTBRa0U0UlRrNE1ESkNNVEl3TUVRME5EYzNSUSJ9.eyJpc3MiOiJodHRwczovL2NzaG9wLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTgxNzU0N2VjNTFiZTBjODkwODA0NjEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU4NTU3NTU1OCwiZXhwIjoxNTg1NTgyNzU4LCJhenAiOiI1NFNSenJPWVpvOVFlTEY3b1A0ZFBXckxuaWptNmRJRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicG9zdDphY3RvcnMiXX0.N2RUmjJeT--3YpUW7M5QXoqICLJieDHeIRSP0THAOkFnwuExC-A1WkzmyFo2UkYaCQxtrPs8qm5OE5pHNwSd_owIHR8piA-GzExVhonD2jB5EUAVbdHn8uePZgA3RbBnV7H5QG0zW25UFjtuHYw8e9d1VgRiinwXQn5peNAgZfw79abw4T2SLpVtVGNpg7gOOaosqSQLc2n5ClhRAzZCTnP1pCKuTNEblXQgBRMgtyx1Izg5vRSMYgDJ7JcVUo5CEP10QW1UxYnYD78NBQco15hWLzSzvf5EkQMJtiu1WADGVXMCqMlO-pfM5o65vixdz-1bv2xdWYt_wS5Tbcof9Q"}
        self.header_assistant = {"Authorization":"Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5EZEJOVFJFTlRRMlJqRkVNRFV4UlVZMlFqVTBRa0U0UlRrNE1ESkNNVEl3TUVRME5EYzNSUSJ9.eyJpc3MiOiJodHRwczovL2NzaG9wLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTgxNzUwNmVjNTFiZTBjODkwODAzNjYiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU4NTU3NTEwNiwiZXhwIjoxNTg1NTgyMzA2LCJhenAiOiI1NFNSenJPWVpvOVFlTEY3b1A0ZFBXckxuaWptNmRJRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.VRshi8QQEsgY__NjIVvQZld9V19QU8XrCw1UDURoPyI3CNQrGDfruyRD1x5-WiEOpj3MJWwYHnpLGxecfAl9uAXAqP_FvgoK-_E_r6F2IpGP5VqSoGKp-QeP_d8PGe2SDmjPRHGONiVjJuWTPP9XxZKMBL8ameS9uHOt1HwFpIQZ0Ri6_plrzuuGPThCsQLnyEaVpeMLIQGwt5-PgyGAHFzwhdJYH6bgp472_wJP_iC7VdOx2Y2Hhkwvv5QK3p2YYwTeoFDmRW3NzlPSlfjQhI8StpzERmbhwSCKlcCymTBvb7QTSKvO3DxDKUxNyJQDccWUofuOY_LgY31oKp2DeA"}
        self.header_producer = {"Authorization":"Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5EZEJOVFJFTlRRMlJqRkVNRFV4UlVZMlFqVTBRa0U0UlRrNE1ESkNNVEl3TUVRME5EYzNSUSJ9.eyJpc3MiOiJodHRwczovL2NzaG9wLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTgxNzViNjkxOGVjMzBjYjE0YmY2M2QiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTU4NTU3Mjc5NywiZXhwIjoxNTg1NTc5OTk3LCJhenAiOiI1NFNSenJPWVpvOVFlTEY3b1A0ZFBXckxuaWptNmRJRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.EhbbxvBQ3PUCinsYwzv58WMLoLIn57A-roqMr15wR9IlmQpEZMzqb7rKhP8yjI9YZkDPcKCSOs1mPGMsKF5P3NCEK3DUVDxEd9JzS0dk_19FNdGzbeH_lBvS1ARYcaWxejn8K7GsNLBYuySo7Pcae4h2-QHYWI9stx-DSEiXXi3LnXULv7CuN4RKfxUQ_0aWvUNBcHg_FsHXN2D13bKVbtDqWEy_gk3aq2QTV14N9g2qMPliWvmpYfBfNn4MHdYyLbQRXqdDFoxGlaXhtrFGpF-UEuMdXyv95kjhlzjaxL0ZEfpqOxQmgpl-FYpW-r64W4k3CKXWbqZycIpwjaAdOA"}
    def tearDown(self):
        """Executed after reach test"""
        pass
    

    # Tests for success behaviour of each endpoint

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.header_producer)
        self.assertEqual(res.status_code, 200)
    
    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.header_producer)
        self.assertEqual(res.status_code, 200)
    
    def test_post_actors(self):
        res = self.client().post('/actors', headers=self.header_producer, json=self.actor)
        self.assertEqual(res.status_code,200)
    
    def test_post_movies(self):
        res = self.client().post('/movies', headers=self.header_producer, json=self.movie)
        self.assertEqual(res.status_code,200)
    
    def test_patch_actors(self):
        res = self.client().patch('/actors/1', headers=self.header_producer, json=self.actor)
        self.assertEqual(res.status_code,200)
    
    def test_patch_movies(self):
        res = self.client().patch('/movies/1', headers=self.header_producer, json=self.movie)
        self.assertEqual(res.status_code,200)
    
    def test_delete_actors(self):
        res = self.client().delete('/actors/1', headers=self.header_producer)
        self.assertEqual(res.status_code,200)
    
    def test_patch_movies(self):
        res = self.client().delete('/movies/1', headers=self.header_producer)
        self.assertEqual(res.status_code,200)

# Tests for error behaviour of each endpoint
    
    def test_get_actors(self):
        res = self.client().get('/actors')
        #data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
    
    def test_get_movies(self):
        res = self.client().get('/movies')
        #data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
    
    def test_post_actors(self):
        res = self.client().post('/actors', json=self.actor)
        self.assertEqual(res.status_code,403)
    
    def test_post_movies(self):
        res = self.client().post('/movies', json=self.movie)
        self.assertEqual(res.status_code,403)
    
    def test_patch_actors(self):
        res = self.client().patch('/actors/1', json=self.actor)
        self.assertEqual(res.status_code,403)
    
    def test_patch_movies(self):
        res = self.client().patch('/movies/1', json=self.movie)
        self.assertEqual(res.status_code,403)
    
    def test_delete_actors(self):
        res = self.client().delete('/actors/1', json=self.actor)
        self.assertEqual(res.status_code,403)
    
    def test_patch_movies(self):
        res = self.client().delete('/movies/1', json=self.movie)
        self.assertEqual(res.status_code,403)

# RBAC test

    def test_casting_assistant_1(self):
        res = self.client().get('/actors', headers=self.header_assistant)
        self.assertEqual(res.status_code, 200)

    def test_casting_assistant_2(self):
        res = self.client().delete('/actors/2', headers=self.header_assistant)
        self.assertEqual(res.status_code, 401)

    def test_casting_assistant(self):
        res = self.client().delete('/actors/2', headers=self.header_director)
        self.assertEqual(res.status_code, 200)
    
    def test_casting_assistant(self):
        res = self.client().delete('/movies/2', headers=self.header_director)
        self.assertEqual(res.status_code, 401)

    def test_executive_producer(self):
        res = self.client().delete('/actors/5', headers=self.header_producer)
        self.assertEqual(res.status_code,200)
    
    def test_executive_producer(self):
        res = self.client().delete('/movies/5', headers=self.header_producer)
        self.assertEqual(res.status_code,200)

if __name__ == "__main__":
    unittest.main()