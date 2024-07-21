from http import HTTPStatus

from flask import Flask, render_template, url_for, redirect, request, Blueprint
import requests

auth_front = Blueprint('auth_front', __name__)
BASE_URL = "http://localhost:5433"
GET_LOGIN = BASE_URL + "/auth/login"
REGISTER_URL = BASE_URL + "/auth/register"


@auth_front.route('/')
def hello_world():
    return redirect(url_for('main.auth_front.login'))


@auth_front.route('/home')
def home():
    return "hola"


@auth_front.route('/register', methods=['GET', 'POST'])
def register():
    created = False
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        response = requests.post(REGISTER_URL, json={
            'username': username,
            'email': email,
            'password': password
        })

        if response.status_code == HTTPStatus.CREATED:
            created = True
        else:
            error_message = response.json().get('message', 'Registration failed')
            return f"Error: {error_message}", response.status_code


    return render_template('register/register.html', created=created)


@auth_front.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['email']
        password = request.form['password']

        response = requests.post(GET_LOGIN, json={"email": user, "password": password})

        if response.status_code == 200:
            return redirect(url_for('main.auth_front.home'))
        else:
            error_message = response.json().get('message', 'Login failed')
            return f"Error: {error_message}", response.status_code

    return render_template('login/login.html')
