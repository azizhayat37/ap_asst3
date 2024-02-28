from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create a Flask app
app = Flask(__name__)

#Filters for Jinja2 template engine
def format_currency(value):
    try:
        return "{:,.2f}".format(float(value))
    except ValueError:
        return value
    
# Register the function as a filter for Jinja2
app.jinja_env.filters['format_currency'] = format_currency

# configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/azizhayat/Documents/AP_ASST3/instance/my_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'secret_key'  # change later when necessary

# instantiate database
db = SQLAlchemy(app)

# create all the models in the database
with app.app_context():
    from models import IndexData
    db.create_all()

# import all routes (keeping it off of app.py)
from routes import *