import datetime

from backend.database.configs.database import db

class Resenias(db.Model):
    __tablename__ = 'resenias'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    comment = db.Column(db.String(32000))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    rating = db.Column(db.Integer, db.CheckConstraint("rating >= 1"))
    paquete_id = db.Column(db.Integer, db.ForeignKey('paquetes_turisticos.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    paquetes_turisticos = db.relationship('PaquetesTuristicos', back_populates='resenias')
    usuarios = db.relationship('Usuarios', back_populates='resenias')