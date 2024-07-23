from flask import Flask, render_template, url_for, redirect, Blueprint

reviews_front = Blueprint('reviews_front', __name__)

BASE_URL = "http://localhost:5433"
REVIEWS_URL = BASE_URL + "/reviews"


@reviews_front.route('/reviews')
def reviews():
    return render_template('resenias/resenias.html', reviews=reviews)
