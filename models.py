# coding: utf-8
from sqlalchemy import BigInteger, CheckConstraint, Column, Date, DateTime, Float, ForeignKey, Index, String, Table
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class Account(db.Model):
    __tablename__ = 'accounts'
    __table_args__ = (
        db.CheckConstraint("(`accounttype` in (_utf8mb4'储蓄账户',_utf8mb4'支票账户'))"),
    )

    accountID = db.Column(db.String(6), primary_key=True)
    money = db.Column(db.Float(asdecimal=True), nullable=False)
    settime = db.Column(db.DateTime)
    accounttype = db.Column(db.String(10))


class Checkacc(Account):
    __tablename__ = 'checkacc'

    accountID = db.Column(db.ForeignKey('accounts.accountID', ondelete='CASCADE'), primary_key=True)
    overdraft = db.Column(db.Float(asdecimal=True))


class Saveacc(Account):
    __tablename__ = 'saveacc'

    accountID = db.Column(db.ForeignKey('accounts.accountID', ondelete='CASCADE'), primary_key=True)
    interestrate = db.Column(db.Float)
    savetype = db.Column(db.String(1))



class Bank(db.Model):
    __tablename__ = 'bank'

    bankname = db.Column(db.String(20), primary_key=True)
    city = db.Column(db.String(20), nullable=False)
    money = db.Column(db.Float(asdecimal=True), nullable=False)



t_checkaccounts = db.Table(
    'checkaccounts',
    db.Column('accountID', db.String(6)),
    db.Column('bank', db.String(20)),
    db.Column('accounttype', db.String(10)),
    db.Column('money', db.Float(asdecimal=True)),
    db.Column('settime', db.DateTime),
    db.Column('overdraft', db.Float(asdecimal=True))
)



t_checkstat = db.Table(
    'checkstat',
    db.Column('bank', db.String(20)),
    db.Column('totalmoney', db.Float(asdecimal=True)),
    db.Column('totalcustomer', db.BigInteger, server_default=db.FetchedValue())
)



class Cusforacc(db.Model):
    __tablename__ = 'cusforacc'
    __table_args__ = (
        db.Index('UK', 'bank', 'cusID', 'accounttype'),
    )

    accountID = db.Column(db.ForeignKey('accounts.accountID', ondelete='CASCADE'), primary_key=True, nullable=False)
    bank = db.Column(db.ForeignKey('bank.bankname'))
    cusID = db.Column(db.ForeignKey('customer.cusID'), primary_key=True, nullable=False, index=True)
    visit = db.Column(db.DateTime)
    accounttype = db.Column(db.String(10))

    account = db.relationship('Account', primaryjoin='Cusforacc.accountID == Account.accountID', backref='cusforaccs')
    bank1 = db.relationship('Bank', primaryjoin='Cusforacc.bank == Bank.bankname', backref='cusforaccs')
    customer = db.relationship('Customer', primaryjoin='Cusforacc.cusID == Customer.cusID', backref='cusforaccs')



t_cusforloan = db.Table(
    'cusforloan',
    db.Column('loanID', db.ForeignKey('loan.loanID', ondelete='CASCADE'), primary_key=True, nullable=False),
    db.Column('cusID', db.ForeignKey('customer.cusID'), primary_key=True, nullable=False, index=True)
)



class Customer(db.Model):
    __tablename__ = 'customer'

    cusID = db.Column(db.String(18), primary_key=True)
    cusname = db.Column(db.String(10), nullable=False)
    cusphone = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(50))
    contact_phone = db.Column(db.String(11), nullable=False)
    contact_name = db.Column(db.String(10), nullable=False)
    contact_Email = db.Column(db.String(20))
    relation = db.Column(db.String(10), nullable=False)
    loanres = db.Column(db.ForeignKey('employee.empID'), index=True)
    accres = db.Column(db.ForeignKey('employee.empID'), index=True)

    employee = db.relationship('Employee', primaryjoin='Customer.accres == Employee.empID', backref='employee_customers')
    employee1 = db.relationship('Employee', primaryjoin='Customer.loanres == Employee.empID', backref='employee_customers_0')
    loan = db.relationship('Loan', secondary='cusforloan', backref='customers')



class Department(db.Model):
    __tablename__ = 'department'

    departID = db.Column(db.String(4), primary_key=True)
    departname = db.Column(db.String(20), nullable=False)
    departtype = db.Column(db.String(15))
    manager = db.Column(db.String(18), nullable=False)
    bank = db.Column(db.ForeignKey('bank.bankname'), nullable=False, index=True)

    bank1 = db.relationship('Bank', primaryjoin='Department.bank == Bank.bankname', backref='departments')



class Employee(db.Model):
    __tablename__ = 'employee'
    __table_args__ = (
        db.CheckConstraint("(`emptype` in (_utf8mb4'0',_utf8mb4'1'))"),
    )

    empID = db.Column(db.String(18), primary_key=True)
    empname = db.Column(db.String(20), nullable=False)
    empphone = db.Column(db.String(11))
    empaddr = db.Column(db.String(50))
    emptype = db.Column(db.String(1))
    empstart = db.Column(db.Date, nullable=False)
    depart = db.Column(db.ForeignKey('department.departID'), index=True)

    department = db.relationship('Department', primaryjoin='Employee.depart == Department.departID', backref='employees')



class Loan(db.Model):
    __tablename__ = 'loan'

    loanID = db.Column(db.String(4), primary_key=True)
    money = db.Column(db.Float(asdecimal=True))
    bank = db.Column(db.ForeignKey('bank.bankname'), index=True)
    state = db.Column(db.String(1), server_default=db.FetchedValue())

    bank1 = db.relationship('Bank', primaryjoin='Loan.bank == Bank.bankname', backref='loans')



t_loanstat = db.Table(
    'loanstat',
    db.Column('bank', db.String(20)),
    db.Column('totalmoney', db.Float(asdecimal=True)),
    db.Column('totalcustomer', db.BigInteger, server_default=db.FetchedValue())
)



class Payinfo(db.Model):
    __tablename__ = 'payinfo'

    loanID = db.Column(db.ForeignKey('loan.loanID', ondelete='CASCADE'), primary_key=True, nullable=False)
    cusID = db.Column(db.ForeignKey('customer.cusID'), primary_key=True, nullable=False, index=True)
    money = db.Column(db.Float(asdecimal=True), primary_key=True, nullable=False)
    paytime = db.Column(db.DateTime, primary_key=True, nullable=False)

    customer = db.relationship('Customer', primaryjoin='Payinfo.cusID == Customer.cusID', backref='payinfos')
    loan = db.relationship('Loan', primaryjoin='Payinfo.loanID == Loan.loanID', backref='payinfos')



t_saveaccounts = db.Table(
    'saveaccounts',
    db.Column('accountID', db.String(6)),
    db.Column('bank', db.String(20)),
    db.Column('accounttype', db.String(10)),
    db.Column('money', db.Float(asdecimal=True)),
    db.Column('settime', db.DateTime),
    db.Column('interestrate', db.Float),
    db.Column('savetype', db.String(1))
)



t_savestat = db.Table(
    'savestat',
    db.Column('bank', db.String(20)),
    db.Column('totalmoney', db.Float(asdecimal=True)),
    db.Column('totalcustomer', db.BigInteger, server_default=db.FetchedValue())
)
