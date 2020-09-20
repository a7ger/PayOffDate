from pymongo import MongoClient
from pprint import pprint
from flask import Flask, request
import json

app = Flask(__name__)

db = MongoClient('mongodb://localhost:27017')['payoffdate']

# items = client['museum']['items']
# pprint(items.find_one())

# db.users.insert_one({
#     'fisrtName' : 'Zack',
#     'lastName' : 'Alger',
#     'username' : 'zackalger',
#     'email' : 'zackalger@gmail.com',
#     'password' : 'password',
# })

# pprint(db.users.find_one({
#     'username' : 'zackalger',
# }))

app = Flask(__name__)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    email = request.json["email"]
    password = request.json["password"]
    
    user = db.users.find_one({
        'email' : email,
        'password' : password,
    })
    
    if user:
        return json.dumps({
            "firstName" : user["firstName"],
            "debts" : user['debts'],
        })

    return "error"

@app.route('/save-debts', methods=['POST'])
def save_debts():
    debts = request.json["debts"]
    email = request.json["email"]
    
    db.users.update_one(
        { 'email': email },
        {
            '$set': {
                'debts': debts
            }
        }
    )
    return "done"    

@app.after_request
def after(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response
