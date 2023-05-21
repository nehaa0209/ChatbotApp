# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the app
app = Flask(__name__, instance_relative_config=True)
app.config["SECRET_KEY"] = '571ebf8e13ca209536c29be68d435c00'
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///C:/Users/neha0/Desktop/UWA SEM 2/Agile Web Development/project2/RestaurantSuggestor/app/chatbot.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Load the config file
app.config.from_object('config')

# Load the views
from app import views
from app import models