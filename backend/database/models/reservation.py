import datetime

from backend.database.configs.database import db


class Reservas(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    status = db.Column(db.String(50), default='activa')
    paquete_id = db.Column(db.Integer, db.ForeignKey('paquetes_turisticos.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
