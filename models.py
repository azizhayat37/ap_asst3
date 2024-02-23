# These models are the Object-Relationship Maps (ORMs) that will be used to populate the database.

from app import db

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    quantity = db.Column(db.Integer)

    def add_quantity(self, quantity):
        self.quantity += quantity

class Assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10))
    price = db.Column(db.Float, nullable=True)
    
    def determine_histoical_price_data(self, ticker):
        if ticker == 'SP500':
            self.price = db.relationship('IndexData', backref='sp500', lazy=True)
        elif ticker == 'VIX':
            self.price = db.relationship('VIXData', backref='vix', lazy=True)

class IndexData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    ticker = db.Column(db.String(10))
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)

    
class VIXData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    ticker = db.Column(db.String(10), default='VIX')
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)

