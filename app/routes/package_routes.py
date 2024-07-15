import datetime
from flask import Blueprint, request, jsonify
from app.models.package import PaquetesTuristicos
from app import db

paquetes_turisticos_bp = Blueprint('paquetes_turisticos', __name__)


# ruta para crear un nuevo paquete turístico
@paquetes_turisticos_bp.route('/', methods=['POST'])
def create_paquete_turistico():
    try:
        data = request.get_json()
        paquete_turistico = PaquetesTuristicos(
            destino_id=data['destino_id'],
            name=data['name'],
            description=data['description'],
            price=data['price'],
            image_url=data['image_url'],
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


# ruta para obtener todos los paquetes turísticos
@paquetes_turisticos_bp.route('/', methods=['GET'])
def get_paquetes_turisticos():
    try:
        paquetes_turisticos = PaquetesTuristicos.query.all()
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
        return jsonify({'paquetes_turisticos': paquetes_turisticos_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
