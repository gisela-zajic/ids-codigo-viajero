from flask import Blueprint, request, jsonify
from app.models.package import PaquetesTuristicos
from app import db

paquetes_turisticos_bp = Blueprint('paquetes_turisticos', __name__)


# ruta para obtener todos los paquetes turísticos
@paquetes_turisticos_bp.route('/', methods=['GET'])
def get_paquetes_turisticos():
    try:
        paquetes_turisticos = PaquetesTuristicos.query.all()
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
