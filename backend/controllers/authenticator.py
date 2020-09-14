# from pymongo import MongoClient
# # pprint library is used to make the output look more pretty
# from pprint import pprint

# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'hello world'

# # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
# db = MongoClient('mongodb://localhost:27010')['payoffdate']
# # db=client.admin
# # # Issue the serverStatus command and print the results
# # serverStatusResult=db.command("serverStatus")
# # pprint(serverStatusResult)

# # items = client['museum']['items']
# # pprint(items.find_one())

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

from flask import Flask
app = Flask(__name__)

@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'

@app.after_request
def after(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response