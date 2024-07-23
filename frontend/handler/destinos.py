from flask import Flask, render_template, url_for, redirect, Blueprint

destinos_front = Blueprint('destinos_front', __name__)

BASE_URL = "http://localhost:5433"
DESTINOS_URL = BASE_URL + "/destinos"


@destinos_front.route('/destinos/<int:user_id>')
def destinos(user_id):
    return render_template('destinos/destinos.html', user_id=user_id)
