# install Postman local for testing 

# flask run
# Postman Testing: POST -> localhost:5000/add -> Body -> raw -> Text -> JSON 
# {
#    "x": 5,
#    "y": 6
#   }

from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def check_posted_data(posted_data, function_name):
    if function_name is "add" or function_name is "subtract" or function_name is "multiply" or function_name is "divide":
        if "x" not in posted_data or "y" not in posted_data:
            return 301 # missing parameter
        else:
            return 200
    elif function_name is "divide":
        if "x" not in posted_data or "y" not in posted_data:
            return 301
        elif int(posted_data["y"]) is 0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        # Get posted data
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data, "add")
        if status_code is not 200:
            error_message = {
                "Message" : "An error has happened",
                "Status Code" : status_code
            }
            return jsonify(error_message)

        x = int(posted_data['x'])
        y = int(posted_data['y'])
        # add the posted data
        result = x + y
        result_dict = {
            'Sum' : result,
            'Status Code' : 200
        }
        return jsonify(result_dict)

class Subtract(Resource):
    def post(self):
        # Get posted data
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data, "subtract")
        if status_code is not 200:
            error_message = {
                "Message" : "An error has happened",
                "Status Code" : status_code
            }
            return jsonify(error_message)

        x = int(posted_data['x'])
        y = int(posted_data['y'])
        # subtract the posted data
        result = x - y
        result_dict = {
            'Sum' : result,
            'Status Code' : 200
        }
        return jsonify(result_dict)

class Multiply(Resource):
    def post(self):
        # Get posted data
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data, "multiply")
        if status_code is not 200:
            error_message = {
                "Message" : "An error has happened",
                "Status Code" : status_code
            }
            return jsonify(error_message)

        x = int(posted_data['x'])
        y = int(posted_data['y'])
        # multiply the posted data
        result = x * y
        result_dict = {
            'Sum' : result,
            'Status Code' : 200
        }
        return jsonify(result_dict)

class Divide(Resource):
    def post(self):
        # Get posted data
        posted_data = request.get_json()

        status_code = check_posted_data(posted_data, "divide")
        if status_code is not 200:
            error_message = {
                "Message" : "An error has happened",
                "Status Code" : status_code
            }
            return jsonify(error_message)

        x = int(posted_data['x'])
        y = int(posted_data['y'])
        # divide the posted data
        result = float(x) / y
        result_dict = {
            'Sum' : result,
            'Status Code' : 200
        }
        return jsonify(result_dict)

api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(host='0.0.0.0')