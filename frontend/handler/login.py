from flask import Flask, render_template, url_for, redirect, request, Blueprint
import requests

auth_front = Blueprint('auth_front', __name__)
BASE_URL = "http://localhost:5433"
GET_LOGIN = BASE_URL + "/auth/login"


@auth_front.route('/')
def hello_world():
    return redirect(url_for('main.auth_front.login'))


@auth_front.route('/home')
def home():
    return "hola"


@auth_front.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['email']
        password = request.form['password']

        response = requests.post(GET_LOGIN, json={"email": user, "password": password})

        if response.status_code == 200:
            return redirect(url_for('main.auth_front.home'))

    return render_template('login/login.html')
