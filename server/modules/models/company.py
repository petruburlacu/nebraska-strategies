from datetime import datetime
from modules.data_access.database import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(80), nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    total_market_value = db.Column(db.Float, nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'company': self.company,
            'ticker': self.ticker,
            'price': self.price,
            'total_market_value': self.total_market_value,
            'shares': self.shares,
            'date_created': self.date_created.isoformat()
        }
    
    def __repr__(self):
        return '<Company %r>' % self.company
    
    def __init__(self, company, ticker, price, shares, date_created):
        self.company = company
        self.ticker = ticker
        self.price = price
        self.total_market_value = price * shares
        self.shares = shares
        self.date_created = date_created