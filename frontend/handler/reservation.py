from flask import Flask, render_template, url_for, redirect, Blueprint

reservas_front = Blueprint('reservas_front', __name__)

BASE_URL = "http://localhost:5433"
RESERVAS_URL = BASE_URL + "/reservas"


@reservas_front.route('/<int:user_id>')
def reservas(user_id):
    if user_id is None:
        return redirect(url_for('main.auth_front.login'))
    return render_template('reservas/reservas.html', user_id=user_id)
