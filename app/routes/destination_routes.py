from flask import Blueprint, request, jsonify
from app.models.destination import Destinos

destinos_bp = Blueprint('destinos', __name__)


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
