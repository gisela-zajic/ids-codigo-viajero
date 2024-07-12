from flask import Blueprint, request, jsonify
from app.models.reservation import Reservas
from app import db

reservas_bp = Blueprint('reservas', __name__)


# ruta para obtener todas las reservas
@reservas_bp.route('/', methods=['GET'])
def get_reservas():
    try:
        reservas = Reservas.query.all()
        reservas_data = []
        for reserva in reservas:
            reserva_data = {
                'id': reserva.id,
                'created_at': reserva.created_at,
                'status': reserva.status,
                'paquete_id': reserva.paquete_id,
                'user_id': reserva.user_id,
            }
            reservas_data.append(reserva_data)
        return jsonify({'reservas': reservas_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
