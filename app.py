from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# create a Flask app
app = Flask(__name__)

# configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/azizhayat/Documents/AP_ASST3/instance/my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'secret_key'  # Replace 'your-secret-key-here' with a strong, unique key.

# set the database URI
db = SQLAlchemy(app)

# create all the models in the database
with app.app_context():
    from models import IndexData
    db.create_all()

from routes import *