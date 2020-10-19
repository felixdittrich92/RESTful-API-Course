"""
Registration of a user
Each user get 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on out database for 1 token
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

class Register(Resource):
    def get(self):
        posted_data = request.get_json()

        # Get the data
        username = posted_data["username"]
        password = posted_data["password"]

        # hash (password + salt) = wdwdwd776rgr9dwdw0d8
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

        # Store username and pw into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "", 
            "Tokens": 6
        })
        json = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(json)

class Store(Resource):
    def post(self):
        posted_data = request.get_json()

        # read the data
        username = posted_data["username"]
        password = posted_data["password"]
        sentence = posted_data["sentence"]

        # verify username and password match
        correct_pw = verify(username, password)

        if not correct_pw:
            json = {
                "status": 302
            }
            return jsonify(json)

        # verify user has enough tokens
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            json = {
                "status": 301
            }
            return jsonify(json)

        # store the sentence and return 200 ok
        users.update({
            "Username": username
        }, 
        {
            "$set":{
                "Sentence":sentence,
                "Tokens": num_tokens - 1
                }
            })

        json = {
            "status": 200,
            "msg": "Sentence saved successfully"
        }
        return jsonify(json)

api.add_resource(Register, '/register')

if __name__ == "__main__":
    app.run(host='0.0.0.0')


