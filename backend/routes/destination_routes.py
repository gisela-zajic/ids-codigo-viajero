import datetime
from flask import Blueprint, request, jsonify
from backend.database.models.destination import Destinos
from backend.database.configs.database import db

destinos_bp = Blueprint('destinos', __name__)


# ruta para crear un nuevo destino
@destinos_bp.route('/', methods=['POST'])
def create_destino():
    try:
        data = request.get_json()

        # valido que se envien todos los datos necesarios
        if not data or not all(key in data for key in ('name', 'description', 'location', 'image_url')):
            return jsonify({'message': 'Faltan datos necesarios'}), 400

        name = data['name']
        description = data['description']
        location = data['location']
        image_url = data['image_url']

        # valido que name y location no esten vacios
        if not name or not location:
            return jsonify({'message': 'El nombre y la ubicación son obligatorios'}), 400

        destino = Destinos(
            name=name,
            description=description,
            location=location,
            image_url=image_url,
            created_at=data.get('created_at', datetime.datetime.now())
        )
        db.session.add(destino)
        db.session.commit()
        return jsonify({'message': 'Destino creado correctamente', 'destino': destino.id}), 201
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500


# ruta para obtener un destino por su id
@destinos_bp.route('/<int:id>', methods=['GET'])
def get_destino(id):
    try:
        destino = Destinos.query.get(id)
        if destino is None:
            return jsonify({'message': 'El destino no fue encontrado'}), 404
        destino_data = {
            'id': destino.id,
            'name': destino.name,
            'description': destino.description,
            'location': destino.location,
            'image_url': destino.image_url,
            'created_at': destino.created_at
        }
        return jsonify(destino_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


# ruta para actualizar un destino
@destinos_bp.route('/<int:id>', methods=['PUT'])
def update_destino(id):
    try:
        destino = Destinos.query.get(id)
        if destino is None:
            return jsonify({'message': 'El destino no fue encontrado'}), 404

        data = request.get_json()
        destino.name = data.get('name', destino.name)
        destino.description = data.get('description', destino.description)
        destino.location = data.get('location', destino.location)
        destino.image_url = data.get('image_url', destino.image_url)
        destino.created_at = data.get('created_at', destino.created_at)

        db.session.commit()
        return jsonify({'message': 'Destino actualizado correctamente'}), 200
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


# ruta para eliminar un destino
@destinos_bp.route('/<int:id>', methods=['DELETE'])
def delete_destino(id):
    try:
        destino = Destinos.query.get(id)
        if destino is None:
            return jsonify({'message': 'El destino no fue encontrado'}), 404

        db.session.delete(destino)
        db.session.commit()
        return jsonify({'message': 'Destino eliminado correctamente'}), 200
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500
