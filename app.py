from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import config
from models import db
from datetime import datetime, date
from init_db import init_data
from models import Bank, Customer, Account, Saveacc, Checkacc, Cusforacc, Loan, Cusforloan, Employee, Payinfo
from sqlalchemy import func
import calendar

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

@app.route('/customer/search', methods=['GET', 'POST'])
def customer_search():
    labels = ["注册银行", "客户姓名", "身份证号", "联系电话", "家庭住址", 
                "联系人姓名", "联系人手机号", "联系人Email", "联系人关系"]
    names = ["bank", "cusname", "cusID", "cusphone", "address",
             "contact_name", "contact_phone", "contact_email", "relation"]
    if request.method == 'GET':
        init_form = {'cusname': '', 'cusID': '', 'cusphone': ''}
        customers = Customer.query.all()
        return render_template('customer/search.html', init_form=init_form, customers=customers, labels=labels, names=names)
    if request.method == 'POST':
        cusID = request.form['cusID']
        cusname = request.form['cusname']
        cusphone = request.form['cusphone']
        customers = Customer.query.filter_by()
        if 'and' in request.form:
            if cusID:
                customers = customers.filter_by(cusID=cusID)
            if cusname:
                customers = customers.filter_by(cusname=cusname)
            if cusphone:
                customers = customers.filter_by(cusphone=cusphone)
        else:
            if cusID or cusname or cusphone:
                customers = customers.filter((Customer.cusID == cusID) | (Customer.cusname == cusname) | 
                    (Customer.cusphone == cusphone))
        return render_template('customer/search.html', customers=customers.all(), init_form=request.form, labels=labels, names=names)

@app.route('/customers/update', methods=['POST'])
def customer_update():
    errors = []
    bank = request.form['bank']
    cusID = request.form['cusID']
    cusname = request.form['cusname']
    cusphone = request.form['cusphone']
    address = request.form['address']
    contact_phone = request.form['contact_phone']
    contact_name = request.form['contact_name']
    contact_email = request.form['contact_email']
    relation = request.form['relation']
    if len(cusID) != 18:
        errors.append('cusID')
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
    if not errors:
        Customer.query.filter_by(cusID=cusID).update(dict(cusID=cusID, cusname=cusname, cusphone=cusphone, 
            address=address, contact_name=contact_name, contact_phone=contact_phone, 
            contact_email=contact_email, relation=relation, bank=bank))
        db.session.commit()
        flash('Update customer ' + cusID + ' successfully!')
        return redirect(url_for('customer_search'))
    else:
        flash('Update customer ' + cusID + ' unsuccessfully!')
        return redirect(url_for('customer_search'))

@app.route('/customers/delete/<cusID>')
def customer_delete(cusID):
    cus = Customer.query.filter_by(cusID=cusID)
    try:
        cus.delete()
        db.session.commit()
        flash('Delete customer ' + cusID + ' successfully!')
        return redirect(url_for('customer_search'))
    except:
        flash('Delete customer ' + cusID + ' unsuccessfully!')
        return redirect(url_for('customer_search'))

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


@app.route('/account/search', methods=['GET', 'POST'])
def account_search():
    if request.method == 'GET':
        init_form = {'accountID': '', 'cusID': '', 'accounttype': ''}
        accounts = Account.query.all()
        for acc in accounts:
            setattr(acc, 'bank', acc.cusforacc.bank)
            setattr(acc, 'cusID', acc.cusforacc.cusID)
            if acc.accounttype == 'saveacc':
                setattr(acc, 'interestrate', acc.saveacc.interestrate)
                setattr(acc, 'savetype', acc.saveacc.savetype)
            else:
                setattr(acc, 'overdraft', acc.checkacc.overdraft)
        return render_template('account/search.html', init_form=init_form, accounts=accounts)
    if request.method == 'POST':
        accountID = request.form['accountID']
        cusID = request.form['cusID']
        accounttype = request.form['accounttype']
        accounts = Account.query.filter_by()
        if 'and' in request.form:
            if accountID:
                accounts = account.filter_by(accountID=accountID)
            if cusID:
                accounts = accounts.filter(Account.cusforacc.has(Cusforacc.cusID==cusID))
            if accounttype:
                accounts = accounts.filter_by(accounttype=accounttype)
        else:
            if accountID or cusID:
                accounts = accounts.filter((Account.accountID == accountID) | (Account.cusID == cusID))
            if accounttype:
                accounts = accounts.filter_by(accounttype=accounttype)
        accounts = accounts.all()
        for acc in accounts:
            setattr(acc, 'bank', acc.cusforacc.bank)
            setattr(acc, 'cusID', acc.cusforacc.cusID)
            if acc.accounttype == 'saveacc':
                setattr(acc, 'interestrate', acc.saveacc.interestrate)
                setattr(acc, 'savetype', acc.saveacc.savetype)
            else:
                setattr(acc, 'overdraft', acc.checkacc.overdraft)
        return render_template('account/search.html', init_form=request.form, accounts=accounts)

@app.route('/account/update', methods=['POST'])
def account_update():
    errors = []
    accountID = request.form['accountID']
    cusID = request.form['cusID']
    money = request.form['money']
    bank = request.form['bank']
    accounttype = request.form['accounttype']
    if accounttype == 'saveacc':
        savetype = request.form['savetype']
        interestrate = request.form['interestrate']
    else:
        overdraft = request.form['overdraft']
    if len(accountID) != 6:
        errors.append('accountID')
    try:
        money = float(money)
    except:
        errors.append('money')
    if len(bank) == 0 or len(bank) > 20:
        errors.append('bank')
    if accounttype == 'saveacc':
        try:
            interestrate = float(interestrate)
        except:
            errors.append('interestrate')
    else:
        try:
            overdraft = float(overdraft)
        except:
            errors.append('overdraft')
    if not Customer.query.filter_by(cusID=cusID).first():
        errors.append('cusID')
    if not errors:
        acc = Account.query.filter_by(accountID=accountID)
        b = Bank.query.filter_by(bankname=acc.first().cusforacc.bank)
        b.update(dict(money=b.first().money - acc.first().money + money))
        acc.update(dict(accountID=accountID, money=money, settime=datetime.now(), accounttype=accounttype))
        if accounttype == 'saveacc':
            Saveacc.query.filter_by(accountID=accountID).update(
                dict(accountID=accountID, interestrate=interestrate, savetype=savetype))
        else:
            Checkacc.query.filter_by(accountID=accountID).update(
                dict(accountID=accountID, overdraft=overdraft))
        Cusforacc.query.filter_by(accountID=accountID).update(
            dict(accountID=accountID, cusID=cusID, visit=datetime.now()))
        db.session.commit()
        flash('Update account ' + accountID + ' successfully!')
        return redirect(url_for('account.search'))
    else:
        flash('Update account ' + accountID + ' unsuccessfully!')
        return redirect(url_for('account.search'))

@app.route('/account/delete/<accountID>')
def account_delete(accountID):
    acc = Account.query.filter_by(accountID=accountID)
    b = Bank.query.filter_by(bankname=acc.first().cusforacc.bank)
    b.update(dict(money=b.first().money - acc.first().money))
    Saveacc.query.filter_by(accountID=accountID).delete()
    Checkacc.query.filter_by(accountID=accountID).delete()
    Cusforacc.query.filter_by(accountID=accountID).delete()
    acc.delete()
    db.session.commit()
    flash('Delete account ' + accountID + ' successfully!')
    return redirect(url_for('account_search'))

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

@app.route('/debt/search', methods=['GET', 'POST'])
def debt_search():
    labels = ["贷款号", "身份证号", "贷款金额", "剩余金额", "贷款银行", "贷款状态"]
    names = ["loanID", "cusID", "money", "rest_money", "bank", "state"]
    if request.method == 'GET':
        init_form = {'loanID': '', 'cusID': '', 'state': ''}
        loans = Loan.query.all()
        for loan in loans:
            setattr(loan, 'cusID', loan.cusforloan[0].cusID)
        return render_template('debt/search.html', init_form=init_form, loans=loans, labels=labels, names=names)
    if request.method == 'POST':
        loanID = request.form['loanID']
        cusID = request.form['cusID']
        state = request.form['state']
        loans = Loan.query.filter_by()
        if 'and' in request.form:
            if loanID:
                loans = loans.filter_by(loanID=loanID)
            if cusID:
                loans = loans.filter(Loan.Cusforloan.has(Cusforloan.cusID==cusID))
            if state:
                loans = loans.filter_by(state=state)
        else:
            if cusID or loanID:
                loans = loans.filter(Loan.cusforloan.has(Cusforloan.cusID == cusID) | 
                (Loan.loanID == loanID))
            if state:
                loans = loans.filter_by(state=state)
        loans = loans.all()
        for loan in loans:
            setattr(loan, 'cusID', loan.cusforloan[0].cusID)
        return render_template('debt/search.html', loans=loans, init_form=request.form, labels=labels, names=names)

@app.route('/debt/update', methods=['POST'])
def debt_update():
    errors = []
    loanID = request.form['loanID']
    cusID = request.form['cusID']
    money = request.form['money']
    if len(loanID) != 4:
        errors.append('loanID')
    try:
        money = float(money)
    except:
        errors.append('money')
    if money < 0:
        errors.append('money')
    loan = Loan.query.filter_by(loanID=loanID).first()
    if not loan:
        errors.append('loanID')
    elif loan.state == 'finished':
        errors.append('loanID')
    elif loan.rest_money < money:
        errors.append('loanID')
    if loan.rest_money - money != 0:
        state = 'going'
    else:
        state = 'finished'
    if not errors:
        loan = Loan.query.filter_by(loanID=loanID)
        b = Bank.query.filter_by(bankname=loan.first().bank)
        b.update(dict(money=b.first().money - money))
        loan.update(dict(state=state, rest_money=loan.first().rest_money-money))
        new_payinfo = Payinfo(loanID=loanID, cusID=cusID, money=money, paytime=datetime.now())
        db.session.add(new_payinfo)
        db.session.commit()
        flash('Update loan ' + loanID + ' successfully!')
        return redirect(url_for('debt_search'))
    else:
        flash('Update loan ' + loanID + ' unsuccessfully!')
        return redirect(url_for('debt_search'))

@app.route('/debt/delete<loanID>')
def debt_delete(loanID):
    loan = Loan.query.filter_by(loanID=loanID)
    if loan.first().state == 'going':
        flash('Delete loan ' + loanID + ' unsuccessfully!')
        return redirect(url_for('debt_search'))
    Cusforloan.query.filter_by(loanID=loanID).delete()
    loan.delete()
    db.session.commit()
    flash('Delete loan ' + loanID + ' successfully!')
    return redirect(url_for('debt_search'))

@app.route('/statistics/year')
def statistics_year():
    time = '年份'
    money_stat = []
    cus_stat = []

    end_year = db.session.query(func.max(Customer.settime)).scalar().year
    colors = ['rgba(178, 167, 212, 1)', 'rgba(151, 187, 205, 1)', 'rgba(244, 188, 175, 1)']
    banks = [bank.bankname for bank in Bank.query.all()]
    for y in range(end_year - 4, end_year + 1):
        money_stat.append({
            'period': y, 
            'acc': {bank: db.session.query(func.sum(Account.money)).filter(
                    Account.cusforacc.has(Cusforacc.bank == bank)
                ).filter(
                    Account.settime.between(date(y, 1, 1), date(y, 12, 31))
                ).scalar() for bank in banks}, 
            'loan': {bank: db.session.query(func.sum(Loan.money)).filter(
                    Loan.bank == bank
                ).filter(
                    Loan.settime.between(date(y, 1, 1), date(y, 12, 31))
                ).scalar() for bank in banks}, 
        })
        cus_stat.append({
            'period': y,
            'acc': {bank: db.session.query(func.count(Account.accountID)).filter(
                Account.cusforacc.has(Cusforacc.bank == bank)
            ).filter(
                    Account.settime.between(date(y, 1, 1), date(y, 12, 31))
                ).scalar() for bank in banks},
            'loan': {bank: db.session.query(func.count(Loan.loanID)).filter(
                Loan.bank == bank
            ).filter(
                    Loan.settime.between(date(y, 1, 1), date(y, 12, 31))
                ).scalar() for bank in banks}
        })
    for stat in money_stat:
        for bank in banks:
            if stat['acc'][bank] == None:
                stat['acc'][bank] = 0
            if stat['loan'][bank] == None:
                stat['loan'][bank] = 0
    for stat in cus_stat:
        for bank in banks:
            if stat['acc'][bank] == None:
                stat['acc'][bank] = 0
            if stat['loan'][bank] == None:
                stat['loan'][bank] = 0

    return render_template('statistics.html', banks=banks, colors=colors, money_stat=money_stat, cus_stat=cus_stat, time=time)

@app.route('/statistics/quarter')
def statistics_quarter():
    time = '季度'
    money_stat = []
    cus_stat = []

    end_date = db.session.query(func.max(Customer.settime)).scalar()
    end_year = end_date.year
    end_quarter = (end_date.month - 1) // 3 + 1
    quarters = [str(end_year + (end_quarter - i - 1) // 4) + 
        'Q' + str((end_quarter + 7 - i) % 4 + 1) for i in range(4, -1, -1)]
    colors = ['rgba(178, 167, 212, 1)', 'rgba(151, 187, 205, 1)', 'rgba(244, 188, 175, 1)']
    banks = [bank.bankname for bank in Bank.query.all()]
    
    for q in quarters:
        y = int(q[:4])
        m_start = (int(q[-1]) - 1) * 3 + 1
        m_end = (int(q[-1]) - 1) * 3 + 3
        money_stat.append({
            'period': q, 
            'acc': {bank: db.session.query(func.sum(Account.money)).filter(
                    Account.cusforacc.has(Cusforacc.bank == bank)
                ).filter(
                    Account.settime.between(date(y, m_start, 1), date(y, m_end, calendar.monthrange(y, m_end)[1]))
                ).scalar() for bank in banks}, 
            'loan': {bank: db.session.query(func.sum(Loan.money)).filter(
                    Loan.bank == bank
                ).filter(
                    Loan.settime.between(date(y, m_start, 1), date(y, m_end, calendar.monthrange(y, m_end)[1]))
                ).scalar() for bank in banks}, 
        })
        cus_stat.append({
            'period': q,
            'acc': {bank: db.session.query(func.count(Account.accountID)).filter(
                Account.cusforacc.has(Cusforacc.bank == bank)
            ).filter(
                    Account.settime.between(date(y, m_start, 1), date(y, m_end, calendar.monthrange(y, m_end)[1]))
                ).scalar() for bank in banks},
            'loan': {bank: db.session.query(func.count(Loan.loanID)).filter(
                Loan.bank == bank
            ).filter(
                    Loan.settime.between(date(y, m_start, 1), date(y, m_end, calendar.monthrange(y, m_end)[1]))
                ).scalar() for bank in banks}
        })
    for stat in money_stat:
        for bank in banks:
            if stat['acc'][bank] == None:
                stat['acc'][bank] = 0
            if stat['loan'][bank] == None:
                stat['loan'][bank] = 0
    for stat in cus_stat:
        for bank in banks:
            if stat['acc'][bank] == None:
                stat['acc'][bank] = 0
            if stat['loan'][bank] == None:
                stat['loan'][bank] = 0
    return render_template('statistics.html', banks=banks, colors=colors, money_stat=money_stat, cus_stat=cus_stat, time=time)
        
    
@app.route('/statistics/month')
def statistics_month():
    time = '月份'
    money_stat = []
    cus_stat = []

    end_date = db.session.query(func.max(Customer.settime)).scalar()
    end_year = end_date.year
    end_month = end_date.month
    months = [str(end_year + (end_month - i - 1) // 12) + 
        'M' + str((end_month + 11 - i) % 12 + 1) for i in range(4, -1, -1)]
    colors = ['rgba(178, 167, 212, 1)', 'rgba(151, 187, 205, 1)', 'rgba(244, 188, 175, 1)']
    banks = [bank.bankname for bank in Bank.query.all()]
    for month in months:
        y = int(month[:4])
        m = int(month.split('M')[-1])
        money_stat.append({
            'period': month, 
            'acc': {bank: db.session.query(func.sum(Account.money)).filter(
                    Account.cusforacc.has(Cusforacc.bank == bank)
                ).filter(
                    Account.settime.between(date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1]))
                ).scalar() for bank in banks}, 
            'loan': {bank: db.session.query(func.sum(Loan.money)).filter(
                    Loan.bank == bank
                ).filter(
                    Loan.settime.between(date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1]))
                ).scalar() for bank in banks}, 
        })
        cus_stat.append({
            'period': month,
            'acc': {bank: db.session.query(func.count(Account.accountID)).filter(
                Account.cusforacc.has(Cusforacc.bank == bank)
            ).filter(
                    Account.settime.between(date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1]))
                ).scalar() for bank in banks},
            'loan': {bank: db.session.query(func.count(Loan.loanID)).filter(
                Loan.bank == bank
            ).filter(
                    Loan.settime.between(date(y, m, 1), date(y, m, calendar.monthrange(y, m)[1]))
                ).scalar() for bank in banks}
        })
    for stat in money_stat:
        for bank in banks:
            if stat['acc'][bank] == None:
                stat['acc'][bank] = 0
            if stat['loan'][bank] == None:
                stat['loan'][bank] = 0
    for stat in cus_stat:
        for bank in banks:
            if stat['acc'][bank] == None:
                stat['acc'][bank] = 0
            if stat['loan'][bank] == None:
                stat['loan'][bank] = 0
    return render_template('statistics.html', banks=banks, colors=colors, money_stat=money_stat, cus_stat=cus_stat, time=time)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)