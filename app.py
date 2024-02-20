from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create a Flask app
app = Flask(__name__)

# set the database URI
db = SQLAlchemy(app)

# create all the models in the database
with app.app_context():
    from models import IndexData
    db.create_all()

