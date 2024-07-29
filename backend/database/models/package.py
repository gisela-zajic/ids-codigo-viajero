import datetime

from backend.database.configs.database import db

class PaquetesTuristicos(db.Model):
    __tablename__ = 'paquetes_turisticos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    destino_id = db.Column(db.Integer, db.ForeignKey('destinos.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(32000))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    reservas = db.relationship('Reservas', back_populates='paquetes_turisticos', cascade='all, delete-orphan')
    resenias = db.relationship('Resenias', back_populates='paquetes_turisticos', cascade='all, delete-orphan')

    destinos = db.relationship('Destinos', back_populates='paquetes_turisticos')