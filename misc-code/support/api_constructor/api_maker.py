from flask import Flask
from flask_restful import Resource, Api, reqparse 
import pandas as pd 
import sqlite3

# AST = Abstract Syntax Trees, how python code gets compiled post tokenization
# allows you to change python code itself
import ast

app = Flask(__name__)
api = Api(app)




class Keywords(Resource):
    
    def get(self):
        
        return "Helloooo World", 200            # payload, status-code
    
    # def post(self):


# this makes /agent-keywords our entry point into the app

api.add_resource(Keywords, '/agent-keywords')

if __name__ == '__main__':
    app.run()


