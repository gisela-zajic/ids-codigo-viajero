import datetime
from flask import Blueprint, request, jsonify
from backend.app.models.package import PaquetesTuristicos
from backend.app.models.destination import Destinos
from backend.app import db

paquetes_turisticos_bp = Blueprint('paquetes_turisticos', __name__)

# ruta para obtener los paquetes turísticos de un destino específico
@paquetes_turisticos_bp.route('/destino/<int:id_destino>/')
def get_paquetes_turisticos_by_destino(id_destino):
    try:
        paquetes_turisticos = PaquetesTuristicos.query.where(PaquetesTuristicos.destino_id == id_destino).all()
        if not paquetes_turisticos:
            return jsonify({'message': 'No se encontraron paquetes turísticos'}), 404

        paquetes_turisticos_data = []
        for paquete_turistico in paquetes_turisticos:
            paquete_turistico_data = {
                'id': paquete_turistico.id,
                'destino_id': paquete_turistico.destino_id,
                'name': paquete_turistico.name,
                'description': paquete_turistico.description,
                'price': paquete_turistico.price,
                'image_url': paquete_turistico.image_url,
                'created_at': paquete_turistico.created_at
            }
            paquetes_turisticos_data.append(paquete_turistico_data)
        return paquetes_turisticos_data
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

# ruta para crear un nuevo paquete turístico
@paquetes_turisticos_bp.route('/', methods=['POST'])
def create_paquete_turistico():
    try:
        data = request.get_json()

        # valido que se envíen todos los datos necesarios
        if not data or not all(key in data for key in ('destino_id', 'name', 'description', 'price', 'image_url')):
            return jsonify({'message': 'Faltan datos necesarios'}), 400

        destino_id = data['destino_id']
        name = data['name']
        description = data['description']
        price = data['price']
        image_url = data['image_url']

        # valido que los datos sean válidos
        if not name or not description or price <= 0:
            return jsonify(
                {'message': 'El nombre, la descripción y el precio son obligatorios y deben ser válidos'}), 400

        paquete_turistico = PaquetesTuristicos(
            destino_id=destino_id,
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            created_at=data.get('created_at', datetime.datetime.now())
        )
        db.session.add(paquete_turistico)
        db.session.commit()
        return jsonify({'message': 'Paquete turístico creado correctamente', 'paquete_turistico': paquete_turistico.id}), 201
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500


# ruta para obtener un paquete turístico por su id
@paquetes_turisticos_bp.route('/<int:id>', methods=['GET'])
def get_paquete_turistico(id):
    try:
        paquete_turistico = PaquetesTuristicos.query.get(id)
        if paquete_turistico is None:
            return jsonify({'message': 'El paquete turístico no fue encontrado'}), 404
        paquete_turistico_data = {
            'id': paquete_turistico.id,
            'destino_id': paquete_turistico.destino_id,
            'name': paquete_turistico.name,
            'description': paquete_turistico.description,
            'price': paquete_turistico.price,
            'image_url': paquete_turistico.image_url,
            'created_at': paquete_turistico.created_at
        }
        return jsonify(paquete_turistico_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


# ruta para actualizar un paquete turístico
@paquetes_turisticos_bp.route('/<int:id>', methods=['PUT'])
def update_paquete_turistico(id):
    try:
        paquete_turistico = PaquetesTuristicos.query.get(id)
        if paquete_turistico is None:
            return jsonify({'message': 'El paquete turístico no fue encontrado'}), 404

        data = request.get_json()
        paquete_turistico.destino_id = data.get('destino_id', paquete_turistico.destino_id)
        paquete_turistico.name = data.get('name', paquete_turistico.name)
        paquete_turistico.description = data.get('description', paquete_turistico.description)
        paquete_turistico.price = data.get('price', paquete_turistico.price)
        paquete_turistico.image_url = data.get('image_url', paquete_turistico.image_url)
        paquete_turistico.created_at = data.get('created_at', paquete_turistico.created_at)

        db.session.commit()
        return jsonify({'message': 'Paquete turístico actualizado correctamente'}), 200
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500


# ruta para obtener todos los paquetes turísticos
@paquetes_turisticos_bp.route('/', methods=['GET'])
def get_paquetes_turisticos():
    try:
        paquetes_turisticos = db.session.query(PaquetesTuristicos, Destinos.name).filter(PaquetesTuristicos.destino_id == Destinos.id).all()
        
        if not paquetes_turisticos:
            return jsonify({'message': 'No se encontraron paquetes turísticos'}), 404

        paquetes_turisticos_data = []
        for paquete_turistico in paquetes_turisticos:
            paquete_turistico_data = {
                'id': paquete_turistico[0].id,
                'destino': paquete_turistico[1],
                'name': paquete_turistico[0].name,
                'description': paquete_turistico[0].description,
                'price': paquete_turistico[0].price,
                'image_url': paquete_turistico[0].image_url,
                'created_at': paquete_turistico[0].created_at
            }
            paquetes_turisticos_data.append(paquete_turistico_data)
        return jsonify({'paquetes_turisticos': paquetes_turisticos_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


# ruta para eliminar un paquete turístico
@paquetes_turisticos_bp.route('/<int:id>', methods=['DELETE'])
def delete_paquete_turistico(id):
    try:
        paquete_turistico = PaquetesTuristicos.query.get(id)
        if paquete_turistico is None:
            return jsonify({'message': 'El paquete turístico no fue encontrado'}), 404

        db.session.delete(paquete_turistico)
        db.session.commit()
        return jsonify({'message': 'Paquete turístico eliminado correctamente'}), 200
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500
