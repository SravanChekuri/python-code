from flask import Flask
from flask_cors import CORS

Flask_app = Flask(__name__)
cors = CORS(Flask_app)

from app import routes

