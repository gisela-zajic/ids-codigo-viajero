from flask import Flask, render_template, url_for, redirect, Blueprint

destinos_front = Blueprint('destinos_front', __name__)

BASE_URL = "http://localhost:5433"
DESTINOS_URL = BASE_URL + "/destinos"


@destinos_front.route('/destinos')
def destinos():
    return render_template('destinos/destinos.html')
