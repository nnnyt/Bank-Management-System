import random, string
from datetime import date


def fake_bank():
    return [
        {'bankname': 'bank1', 'city': 'Shanghai', 'money': 1010996},
        {'bankname': 'bank2', 'city': 'Hefei', 'money': 2919283},
        {'bankname': 'bank3', 'city': 'Beijing', 'money': 2736421},
    ]

def fake_department():
    return [
        {'departID': '1111', 'departname': 'department1', 'departtype': 'type1', 'manager': '111111111111111111', 'bank': 'bank1'},
        {'departID': '2222', 'departname': 'department2', 'departtype': 'type2', 'manager': '222222222222222222', 'bank': 'bank2'},
        {'departID': '3333', 'departname': 'department3', 'departtype': 'type1', 'manager': '333333333333333333', 'bank': 'bank3'},
        {'departID': '4444', 'departname': 'department4', 'departtype': 'type2', 'manager': '444444444444444444', 'bank': 'bank1'}
    ]

def fake_emp(depart_data, num=10):
    emp_data = []
    for m in depart_data:
        emp = {
            'empID': m['manager'],
            'empname': ''.join(random.choices(string.ascii_letters, k=random.randint(3, 10))),
            'emptype': 'manager',
            'empstart': date(random.randint(2015, 2020), random.randint(1, 12), random.randint(1, 28)), 
            'depart': m['departID']
        }
        emp_data.append(emp)
    for _ in range(num):
        depart = random.choice(depart_data)
        emp = {
            'empID': ''.join(random.choices(string.digits, k=18)),
            'empname': ''.join(random.choices(string.ascii_letters, k=random.randint(3, 10))),
            'emptype': 'staff',
            'empstart': date(random.randint(2015, 2020), random.randint(1, 12), random.randint(1, 28)), 
            'depart': depart['departID']
        }
        emp_data.append(emp)
    return emp_data
    
def fake_cus(bank_data, emp_data, num=100):
    cus_data = []
    for _ in range(num):
        bank = random.choice(bank_data)
        loan_emp = random.choice(emp_data)
        acc_emp = random.choice(emp_data)
        cus = {
            'cusID': ''.join(random.choices(string.digits, k=18)), 
            'bank': bank['bankname'],
            'settime': date(random.randint(2015, 2020), random.randint(1, 12), random.randint(1, 28)), 
            'cusname': ''.join(random.choices(string.ascii_letters, k=random.randint(3, 10))), 
            'cusphone': ''.join(random.choices(string.digits, k=11)), 
            'address': '', 
            'contact_name': ''.join(random.choices(string.ascii_letters, k=random.randint(3, 10))), 
            'contact_phone': ''.join(random.choices(string.digits, k=11)), 
            'contact_email': '', 
            'relation': ''.join(random.choices(string.ascii_letters, k=random.randint(3, 10))), 
            'loanres': loan_emp['empID'],
            'accres': acc_emp['empID']
        }
        cus_data.append(cus)
    return cus_data


def fake_acc(bank_data, cus_data, num=100):
    acc_data = []
    cusforacc_data = []
    saveacc_data = []
    checkacc_data = []
    for _ in range(num):
        bank = random.choice(bank_data)
        cus = random.choice(cus_data)
        acc = {
            'accountID': ''.join(random.choices(string.digits, k=6)), 
            'money': random.uniform(100, 10000),
            'settime': date(random.randint(2015, 2020), random.randint(1, 12), random.randint(1, 28)), 
            'accounttype': random.choice(['saveacc', 'checkacc']),
        }
        acc_data.append(acc)
        cusforacc = {
            'accountID': acc['accountID'],
            'cusID': cus['cusID'],
            'bank': bank['bankname']
        }
        cusforacc_data.append(cusforacc)
        if acc['accounttype'] == 'saveacc':
            saveacc = {
                'accountID': acc['accountID'],
                'interestrate': random.uniform(0.01, 0.3),
                'savetype': random.choice(['RMB', 'USD', 'EUR', 'JPY', 'GBP'])
            }
            saveacc_data.append(saveacc)
        else:
            checkacc = {
                'accountID': acc['accountID'],
                'overdraft': random.randint(100, 10000),
            }
            checkacc_data.append(checkacc)

    return acc_data, cusforacc_data, saveacc_data, checkacc_data


def fake_loan(bank_data, cus_data, num=100):
    loan_data = []
    cusforloan_data = []
    for _ in range(num):
        bank = random.choice(bank_data)
        cus = random.choice(cus_data)
        money = random.uniform(100, 10000),
        loan = {
            'loanID': ''.join(random.choices(string.digits, k=4)), 
            'settime': date(random.randint(2015, 2020), random.randint(1, 12), random.randint(1, 28)), 
            'money': money,
            'rest_money': money,
            'bank': bank['bankname'],
            'state': 'waiting',
        }
        loan_data.append(loan)
        cusforloan = {
            'loanID': loan['loanID'],
            'cusID': cus['cusID']
        }
        cusforloan_data.append(cusforloan)
    return loan_data, cusforloan_data


def init_data(db):
    print('Generating data ...')
    from models import Bank, Customer, Account, Saveacc, Checkacc, Cusforacc, Loan, Cusforloan, Department, Employee
    db.session.query(Employee).delete()
    db.session.query(Department).delete()
    db.session.query(Cusforacc).delete()
    db.session.query(Saveacc).delete()
    db.session.query(Checkacc).delete()
    db.session.query(Cusforloan).delete()
    db.session.query(Loan).delete()
    db.session.query(Customer).delete()
    db.session.query(Account).delete()
    db.session.query(Bank).delete()

    bank_data = fake_bank()
    for bank in bank_data:
        if not Bank.query.filter_by(bankname=bank['bankname']).first():
            new_bank = Bank(**bank)
            db.session.add(new_bank)
    
    db.session.commit()

    department_data = fake_department()
    for department in department_data:
        if not Department.query.filter_by(departID=department['departID']).first():
            new_depart = Department(**department)
            db.session.add(new_depart)
    db.session.commit()

    emp_data = fake_emp(department_data)
    for emp in emp_data:
        if not Employee.query.filter_by(empID=emp['empID']).first():
            new_emp = Employee(**emp)
            db.session.add(new_emp)
    db.session.commit()

    cus_data = fake_cus(bank_data, emp_data)
    for cus in cus_data:
        if not Customer.query.filter_by(cusID=cus['cusID']).first():
            new_cus = Customer(**cus)
            db.session.add(new_cus)
    
    db.session.commit()
    
    acc_data, cusforacc_data, saveacc_data, checkacc_data = fake_acc(bank_data, cus_data)
    for acc in acc_data:
        if not Account.query.filter_by(accountID=acc['accountID']).first():
            new_acc = Account(**acc)
            db.session.add(new_acc)
    for cusforacc in cusforacc_data:
        if not Cusforacc.query.filter_by(accountID=cusforacc['accountID'], cusID=cusforacc['cusID']).first():
            new_cusforacc = Cusforacc(**cusforacc)
            db.session.add(new_cusforacc)
    for saveacc in saveacc_data:
        if not Saveacc.query.filter_by(accountID=saveacc['accountID']).first():
            new_saveacc = Saveacc(**saveacc)
            db.session.add(new_saveacc)
    for checkacc in checkacc_data:
        if not Checkacc.query.filter_by(accountID=checkacc['accountID']).first():
            new_checkacc = Checkacc(**checkacc)
            db.session.add(new_checkacc)
    
    db.session.commit()
    
    loan_data, cusforloan_data = fake_loan(bank_data, cus_data)
    for loan in loan_data:
        if not Loan.query.filter_by(loanID=loan['loanID']).first():
            new_loan = Loan(**loan)
            db.session.add(new_loan)
    for cusforloan in cusforloan_data:
        if not Cusforloan.query.filter_by(loanID=cusforloan['loanID'], cusID=cusforloan['cusID']).first():
            new_cusforloan = Cusforloan(**cusforloan)
            db.session.add(new_cusforloan)

    db.session.commit()

    print('Generation finished !')
