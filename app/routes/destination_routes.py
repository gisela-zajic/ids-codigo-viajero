import datetime
from flask import Blueprint, request, jsonify
from app.models.destination import Destinos
from app import db

destinos_bp = Blueprint('destinos', __name__)


# ruta para crear un nuevo destino
@destinos_bp.route('/', methods=['POST'])
def create_destino():
    try:
        data = request.get_json()
        destino = Destinos(
            name=data['name'],
            description=data['description'],
            location=data['location'],
            image_url=data['image_url'],
            created_at=data.get('created_at', datetime.datetime.now())
        )
        db.session.add(destino)
        db.session.commit()
        return jsonify({'message': 'Destino creado correctamente', 'destino': destino.id}), 201
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500


# ruta para obtener todos los destinos
@destinos_bp.route('/', methods=['GET'])
def get_destinos():
    try:
        destinos = Destinos.query.all()
        destinos_data = []
        for destino in destinos:
            destino_data = {
                'id': destino.id,
                'name': destino.name,
                'description': destino.description,
                'location': destino.location,
                'image_url': destino.image_url,
                'created_at': destino.created_at
            }
            destinos_data.append(destino_data)
        return jsonify({'destinos': destinos_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
