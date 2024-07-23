from http import HTTPStatus

from flask import render_template, url_for, redirect, request, Blueprint
import requests

dashboard_front = Blueprint('dashboard_front', __name__)

BASE_URL = "http://localhost:5433"
DASHBOARD_URL = BASE_URL + "/dashboard"

@dashboard_front.route('/dashboard')
def dashboard():
    user_id = request.args.get('id')
    if user_id is None:
        return redirect(url_for('main.auth_front.login'))
    return render_template('dashboard/dashboard.html', user_id=user_id)
