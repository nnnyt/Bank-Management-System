from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import config
from models import Account, Checkacc, Saveacc, Bank, Cusforacc, Customer, Department, Employee, Loan, Payinfo
from models import db


app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/client/create')
def client_create():
    init_form = {'cusID': '', 'cusname': '', 'bank': '', 'cusphone': '', 'address': '',
        'contact_phone': '', 'contact_name': '', 'contact_email': '', 'relation': ''}
    return render_template('client/create.html', init_form=init_form)

@app.route('/client/search')
def client_search():
    return render_template('client/search.html')

@app.route('/account/create')
def account_create():
    return render_template('account/create.html')

@app.route('/account/search')
def account_search():
    return render_template('account/search.html')

@app.route('/debt/create')
def debt_create():
    return render_template('debt/create.html')

@app.route('/debt/search')
def debt_search():
    return render_template('debt/search.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)