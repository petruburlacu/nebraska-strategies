from datetime import datetime
from flask import Flask, jsonify, render_template
from modules.config.logger_config import logger
from modules.data_access.financial_screener import get_market_data
from modules.models.company import Company
from modules.data_access.database import db

# app = Flask(__name__, static_folder='static', template_folder='static/build')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nebraska.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db.init_app(app)

@app.route('/', methods=['GET'])
def all():
    logger.info('Getting all companies')
    companies = Company.query.all()
    return render_template('index.html', companies=companies)

@app.route('/companies', methods=['GET'])
def get_companies():
    logger.info('Getting all companies')
    companies = Company.query.all()
    return jsonify([company.to_dict() for company in companies])

@app.route('/all', methods=['GET'])
def get_all():
    logger.info('Getting all companies')
    #async call to get data: get_market_data
    data = get_market_data()
    return data

if __name__ == '__main__':
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(Company('Apple', 'AAPL', 125.00, 100, datetime.utcnow()))
            db.session.add(Company('Microsoft', 'MSFT', 250.00, 100, datetime.utcnow()))
            db.session.add(Company('Google', 'GOOG', 1500.00, 100, datetime.utcnow()))
            db.session.add(Company('Amazon', 'AMZN', 3000.00, 100, datetime.utcnow()))
            db.session.add(Company('Facebook', 'FB', 250.00, 100, datetime.utcnow()))
            db.session.commit()

        app.config['DEBUG'] = True
        app.run(host='0.0.0.0', port=8080)

