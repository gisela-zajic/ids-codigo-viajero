import datetime
from app import db


class PaquetesTuristicos(db.Model):
    __tablename__ = 'paquetes_turisticos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    destino_id = db.Column(db.Integer, db.ForeignKey('destinos.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(32000))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
