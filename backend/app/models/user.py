import datetime
from backend.app import db


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
