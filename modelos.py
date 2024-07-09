import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())


class Destinos(db.Model):
    __tablename__ = 'destinos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(32000))
    location = db.Column(db.String(100))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default='2024-06-16 00:00:00')


class Paquetes_turisticos(db.Model):
    __tablename__ = 'paquetes_turisticos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    paquetes_turisticos_id = db.Column(db.Integer, db.ForeignKey('destinos.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(32000))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())


class Resenias(db.Model):
    __tablename__ = 'resenias'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    comment = db.Column(db.String(32000))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    rating = db.Column(db.Integer, db.CheckConstraint("rating >= 1"))
    paquete_id = db.Column(db.Integer, db.ForeignKey('paquetes_turisticos.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))


class Reservas(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default='2024-07-01 00:0:00')
    status = db.Column(db.String(50), default='activa')
    paquete_id = db.Column(db.Integer, db.ForeignKey('paquetes_turisticos.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
