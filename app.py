from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import config
from flask_sqlalchemy import SQLAlchemy

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
    return render_template('client.html')

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