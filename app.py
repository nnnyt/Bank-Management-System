from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import config
from models import db
from datetime import datetime
from init_db import init_data
from models import Bank, Customer, Account, Saveacc, Checkacc, Cusforacc, Loan, Cusforloan, Employee

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

with app.app_context():
    db.create_all()
    # init_data(db)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/customer/create', methods=['GET', 'POST'])
def customer_create():
    labels = ["注册银行*", "客户姓名*", "身份证号*", "联系电话*", "家庭住址", 
                "联系人姓名*", "联系人手机号*", "联系人Email", "联系人与客户关系*", "账户负责人", "贷款负责人"]
    names = ["bank", "cusname", "cusID", "cusphone", "address",
                "contact_name", "contact_phone", "contact_email", "relation", "accres", "loanres"]
    init_form = {item: '' for item in names}

    if request.method == 'GET':
        return render_template('customer/create.html', init_form=init_form, labels=labels, names=names)
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
        accres = request.form['accres']
        loanres = request.form['loanres']
        # check whether is invalid
        if len(cusID) != 18 or Customer.query.filter_by(cusID=cusID).first():
            errors.append('cusID')
        if len(bank) == 0 or len(bank) > 20 or (not Bank.query.filter_by(bankname=bank).first()):
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
        if accres is None and not Employee.query.filter_by(empID=accres).first():
            errors.append('accres')
        if loanres is None and not Employee.query.filter_by(empID=loanres).first():
            errors.append('loanres')
        if not errors:
            new_customer = Customer(cusID=cusID, settime=datetime.now(), bank=bank, cusname=cusname, cusphone=cusphone, 
                address=address, contact_name=contact_name, contact_phone=contact_phone, 
                contact_email=contact_email, relation=relation)
            db.session.add(new_customer)
            db.session.commit()
            flash('Create new customer ' + cusID + ' successfully!')
            return render_template('customer/create.html', errors=errors, init_form=init_form, labels=labels, names=names)
        else:
            return render_template('customer/create.html', errors=errors, init_form=request.form, labels=labels, names=names)
    

@app.route('/customer/search')
def customer_search():
    return render_template('customer/search.html')

@app.route('/account/create', methods=['GET', 'POST'])
def account_create():
    labels = ["账户号*", "客户身份证号*", "余额*", "开户银行*", "账户类型*", "货币类型", "利率", "透支额度"]
    names = ["accountID", "cusID", "money", "bank", "accounttype", "savetype", "interestrate", "overdraft"]
    init_form = {item: '' for item in names}

    if request.method == 'GET':
        return render_template('account/create.html', init_form=init_form, labels=labels, names=names)
    if request.method == 'POST':
        errors = []
        accountID = request.form['accountID']
        cusID = request.form['cusID']
        money = request.form['money']
        bank = request.form['bank']
        accounttype = request.form['accounttype']
        savetype = request.form['savetype']
        interestrate = request.form['interestrate']
        overdraft = request.form['overdraft']
        if len(accountID) != 6 or Account.query.filter_by(accountID=accountID).first():
            errors.append('accountID')
        try:
            money = float(money)
        except:
            errors.append('money')
        if len(bank) == 0 or len(bank) > 20 or not Bank.query.filter_by(bankname=bank).first():
            errors.append('bank')
        if accounttype == 'saveacc':
            try:
                interestrate = float(interestrate)
            except:
                errors.append('interestrate')
            if savetype == '':
                errors.append('savetype')
        else:
            try:
                overdraft = float(overdraft)
            except:
                errors.append('overdraft')
        if not Customer.query.filter_by(cusID=cusID).first():
            errors.append('cusID')
        if not errors:
            new_account = Account(accountID=accountID, money=money, settime=datetime.now(), accounttype=accounttype)
            db.session.add(new_account)
            if accounttype == 'saveacc':
                new_saveacc = Saveacc(accountID=accountID, interestrate=interestrate, savetype=savetype)
                db.session.add(new_saveacc)
            else:
                new_checkacc = Checkacc(accountID=accountID, overdraft=overdraft)
                db.session.add(new_checkacc)
            new_cusforacc = Cusforacc(accountID=accountID, cusID=cusID, bank=bank, visit=datetime.now())
            db.session.add(new_cusforacc)
            b = Bank.query.filter_by(bankname=bank)
            b.update(dict(money=b.first().money + money))
            db.session.commit()
            flash('Create new account ' + accountID + ' successfully!')
            return render_template('account/create.html', errors=errors, init_form=init_form, labels=labels, names=names)
        else:
            return render_template('account/create.html', errors=errors, init_form=request.form, labels=labels, names=names)


@app.route('/account/search')
def account_search():
    return render_template('account/search.html')

@app.route('/debt/create' , methods=['GET', 'POST'])
def debt_create():
    labels = ["贷款号*", "身份证号*", "贷款金额*", "贷款银行*"]
    names = ["loanID", "cusID", "money", "bank"]
    init_form = {item: '' for item in names}
    if request.method == 'GET':
        return render_template('debt/create.html', init_form=init_form, labels=labels, names=names)
    if request.method == 'POST':
        errors = []
        loanID = request.form['loanID']
        cusID = request.form['cusID']
        money = request.form['money']
        bank = request.form['bank']
        state = 'waiting'
        if len(loanID) != 4:
            errors.append('loanID')
        try:
            money = float(money)
        except:
            errors.append('money')
        if len(bank) == 0 or len(bank) > 20:
            errors.append('bank')
        if Loan.query.filter_by(loanID=loanID).first():
            errors.append('loanID')
        if not Customer.query.filter_by(cusID=cusID).first():
            errors.append('cusID')
        if not errors:
            new_loan = Loan(loanID=loanID, settime=datetime.now(), money=money, rest_money=money, bank=bank, state=state)
            db.session.add(new_loan)
            new_cusforloan = Cusforloan(loanID=loanID, cusID=cusID)
            db.session.add(new_cusforloan)
            db.session.commit()
            flash('Create new loan ' + loanID + ' successfully!')
            return render_template('debt/create.html', errors=errors, init_form=init_form, labels=labels, names=names)
        else:
            return render_template('debt/create.html', errors=errors, init_form=request.form, labels=labels, names=names)

@app.route('/debt/search')
def debt_search():
    return render_template('debt/search.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)