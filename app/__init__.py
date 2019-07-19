from flask import Flask, render_template, redirect, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# app views

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

from app import routes, models

