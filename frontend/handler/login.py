from http import HTTPStatus

from flask import render_template, url_for, redirect, request, Blueprint
import requests

auth_front = Blueprint('auth_front', __name__)

BASE_URL = "http://localhost:5433"
GET_LOGIN = BASE_URL + "/auth/login"
REGISTER_URL = BASE_URL + "/auth/register"
USER_URL = BASE_URL + "/user"
DELETE_URL = BASE_URL + "auth/delete"


@auth_front.route('/')
def login_page():
    return redirect(url_for('main.auth_front.login'))


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
            user_id = response.json().get('user_id')
            return redirect(url_for('main.dashboard_front.dashboard', user_id=user_id))
            #return redirect(url_for('main.auth_front.home'))
        else:
            error_message = response.json().get('message', 'Login failed')
            return f"Error: {error_message}", response.status_code

    return render_template('login/login.html')


@auth_front.route('/delete/<int:user_id>')
def delete_user(user_id):
    if user_id is None:
        return redirect(url_for('main.auth_front.login'))
    return render_template('delete_user/delete_user.html', user_id=user_id)
