from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import config
from models import Account, Checkacc, Saveacc, Bank, Cusforacc, Customer, Department, Employee, Loan, Payinfo
from models import db
from datetime import datetime


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

@app.route('/customer/create', methods=['GET', 'POST'])
def customer_create():
    if request.method == 'GET':
        init_form = {'cusID': '', 'cusname': '', 'bank': '', 'cusphone': '', 'address': '',
            'contact_phone': '', 'contact_name': '', 'contact_email': '', 'relation': ''}
        return render_template('customer/create.html', init_form=init_form)
    if request.method == 'POST': 
        errors = []
        cusID = request.form['cusID']
        bank = request.form['bank']
        cusname = request.form['cusname']
        cusphone = request.form['cusphone']
        address = request.form['address']
        contact_phone = request.form['contact_phone']
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        relation = request.form['relation']
        if len(cusID) != 18:
            errors.append('cusID')
        if len(bank) == 0 or len(bank) > 20:
            errors.append('bank')
        if len(cusname) == 0 or len(cusname) > 10:
            errors.append('cusname')
        if len(cusphone) != 11:
            errors.append('cusphone')
        if len(address) > 50:
            errors.append('address')
        if len(contact_phone) != 11:
            errors.append('contact_phone')
        if len(contact_name) == 0 or len(contact_name) > 10:
            errors.append('contact_name')
        if len(contact_email) > 0 and '@' not in contact_email:
            errors.append('contact_email')
        if len(relation) == 0 or len(relation) > 10:
            errors.append('relation')
        if Customer.query.filter_by(cusID=cusID).first():
            errors.append('cusID')
        if not errors:
            new_customer = Customer(cusID=cusID, settime=datetime.now(), bank=bank, cusname=cusname, cusphone=cusphone, 
                address=address, contact_name=contact_name, contact_phone=contact_phone, 
                contact_email=contact_email, relation=relation)
            db.session.add(new_customer)
            db.session.commit()
            init_form = {'cusID': '', 'cusname': '', 'bank': '', 'cusphone': '', 'address': '',
                'contact_phone': '', 'contact_name': '', 'contact_email': '', 'relation': ''}
            flash('Create new customer ' + cusID + ' successfully!')
            return render_template('customer/create.html', errors=errors, init_form=init_form)
        else:
            return render_template('customer/create.html', errors=errors, init_form=request.form)
    

@app.route('/customer/search')
def customer_search():
    return render_template('customer/search.html')

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