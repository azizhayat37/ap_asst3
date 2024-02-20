# These models are the Object-Relationship Maps (ORMs) that will be used to populate the database.

from app import db

class IndexData(db.Model):
    date = db.Column(db.String(10), primary_key=True)
    ticker = db.Column(db.String(10))
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
