# These models are the Object-Relationship Maps (ORMs) that will be used to populate the database.

from app import db

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    quantity = db.Column(db.Integer)

    def determine_ticker(self, asset_id):
        return db.session.query(Assets).filter(Assets.id == asset_id).first().ticker
    '''
    price = db.Column(db.Float, nullable=True)
    def set_price(self, asset_id, selected_date):
        if asset_id == 'SP500':
            self.price = db.session.query(IndexData).filter(IndexData.date == selected_date).first().close
        elif asset_id == 'VIX':
            self.price = db.session.query(VIXData).filter(VIXData.date == selected_date).first().close

    def add_asset_quantity(self, quantity):
        self.quantity += quantity
    '''

class Assets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10))
    full_name = db.Column(db.Integer, nullable=True)
    
    def determine_full_name(self, ticker):
        if ticker == 'SP500':
            self.full_name = 'S&P 500 Index ETF'
        elif ticker == 'VIX':
            self.full_name = 'Volatility Index ETF'


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
    ticker = db.Column(db.String(10))
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)

