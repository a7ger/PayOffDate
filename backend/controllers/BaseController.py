from pymongo import MongoClient
from flask import Flask, request

class BaseController:
    db = MongoClient('mongodb://localhost:27010')['payoffdate']
    app = Flask(__name__)
    
    @app.after_request
    def after(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        return response