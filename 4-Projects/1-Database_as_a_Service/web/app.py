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
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]
        hashed_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
     
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens": 6
        })
     
        json = {
            "status":200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(json)
     
def verify_pw(username, password):
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]
     
    if bcrypt.hashpw(password.encode("utf8"), hashed_pw) == hashed_pw:
        return True
    else:
        return False
     
def count_tokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens
     
     
class Store(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]
        sentence = posted_data["sentence"]
     
        correct_pw = verify_pw(username, password)
     
        if not correct_pw:
            json = {
                "status": 302
            }
            return jsonify(json)
     
        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            json = {
                "status": 301
            }
            return jsonify(json)
     
        users.update({
            "Username": username
        }, {
            "$set":{
                "Sentence":sentence,
                "Tokens":num_tokens-1
                }
        })
            
        json = {
            "status":200,
            "msg":"Sentence saved successfully"
        }
        return jsonify(json)
     
class Get(Resource):
    def post(self):
        posted_data = request.get_json()
     
        username = posted_data["username"]
        password = posted_data["password"]
     
        correct_pw = verify_pw(username, password)
     
        if not correct_pw:
            json = {
                "status":302
            }
            return  jsonify(json)
     
        num_tokens = count_tokens(username)
        if num_tokens <= 0:

            json = {
                "status": 301
            }
            return jsonify(json)
     
        sentence = users.find({
            "Username": username
        })[0]["Sentence"]
     
        json = {
            "status": 200,
            "sentence": sentence
        }
        return jsonify(json)
     
     
api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Get, "/get")
     
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
