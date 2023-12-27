from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template
import logging as log

# app = Flask(__name__, static_folder='static', template_folder='static/build')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nebraska.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(80), nullable=False)
    ticker = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'company': self.company,
            'ticker': self.ticker,
            'price': self.price,
            'shares': self.shares,
            'date_created': self.date_created.isoformat()
        }
    
    def __repr__(self):
        return '<Company %r>' % self.company
    
    def __init__(self, company, ticker, price, shares, date_created):
        self.company = company
        self.ticker = ticker
        self.price = price
        self.shares = shares
        self.date_created = date_created


@app.route('/', methods=['GET'])
def all():
    log.info('Getting all companies')
    companies = Company.query.all()
    return render_template('index.html', companies=companies)

@app.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    return jsonify([company.to_dict() for company in companies])

if __name__ == '__main__':
        log.info('Starting app')
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(Company('Apple', 'AAPL', 125.00, 100, datetime.utcnow()))
            db.session.add(Company('Microsoft', 'MSFT', 250.00, 100, datetime.utcnow()))
            db.session.add(Company('Google', 'GOOG', 1500.00, 100, datetime.utcnow()))
            db.session.add(Company('Amazon', 'AMZN', 3000.00, 100, datetime.utcnow()))
            db.session.add(Company('Facebook', 'FB', 250.00, 100, datetime.utcnow()))
            db.session.commit()
        app.run(host='0.0.0.0', debug=True)

