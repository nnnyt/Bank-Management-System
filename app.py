from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import config
from models import Account, Checkacc, Saveacc, Bank, Cusforacc, Customer, Department, Employee, Loan, Payinfo


db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/client')
def client():
    labels = ['ID', '姓名', '联系电话', '地址', '联系人电话', '联系人姓名', '联系人邮箱', '与客户关系', '贷款负责人', '账户负责人']
    result = Customer.query.all()
    return render_template('client.html', labels=labels, content=result)

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/debt')
def debt():
    return render_template('debt.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)