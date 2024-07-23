from http import HTTPStatus

from flask import Flask, render_template, url_for, redirect, request, Blueprint
import requests

auth_front = Blueprint('auth_front', __name__)
reservas_front = Blueprint('reservas_front', __name__)

BASE_URL = "http://localhost:5433"
GET_LOGIN = BASE_URL + "/auth/login"
REGISTER_URL = BASE_URL + "/auth/register"
USER_URL = BASE_URL + "/user"
DELETE_URL = BASE_URL + "/auth/delete"
RESERVAS_URL = BASE_URL + "/reservas"


@auth_front.route('/')
def hello_world():
    return redirect(url_for('main.auth_front.login'))


@auth_front.route('/home')
def home():
    return "Página de inicio"


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
            return redirect(url_for('main.auth_front.dashboard', id=user_id))
            #return redirect(url_for('main.auth_front.home'))
        else:
            error_message = response.json().get('message', 'Login failed')
            return f"Error: {error_message}", response.status_code

    return render_template('login/login.html')


@auth_front.route('/delete', methods=['POST'])
def delete_user():
    user_id = request.form.get('id')

    if user_id:
        try:
            response = requests.delete(f"{DELETE_URL}/{user_id}")

            if response.status_code == HTTPStatus.OK:
                return redirect(url_for('main.auth_front.login'))
            else:
                error_message = response.json().get('message', 'Delete failed')
                return f"Error: {error_message}", response.status_code
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {str(e)}", HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        return "User ID is required", HTTPStatus.BAD_REQUEST


@auth_front.route('/dashboard')
def dashboard():
    user_id = request.args.get('id')
    if user_id is None:
        return redirect(url_for('main.auth_front.login'))
    return render_template('dashboard/dashboard.html', user_id=user_id)


@reservas_front.route('/<int:user_id>')
def reservas(user_id):
    if user_id is None:
        return redirect(url_for('main.auth_front.login'))
    return render_template('reservas/reservas.html', user_id=user_id)
