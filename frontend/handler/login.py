from flask import Flask, render_template, url_for, redirect, request, Blueprint

auth_front = Blueprint('auth_front', __name__)


@auth_front.route('/')
def hello_world():
    return redirect(url_for('main.auth_front.login'))


@auth_front.route('/home')
def home():
    return "hola"


user = "admin@gmail.com"
password = "1234"


@auth_front.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['email'] == user and request.form['password'] == password:
            return redirect(url_for('main.auth_front.home'))
    return render_template('login/login.html')
