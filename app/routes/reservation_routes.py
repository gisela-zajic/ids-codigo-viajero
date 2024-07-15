import datetime
from flask import Blueprint, request, jsonify
from app.models.reservation import Reservas
from app import db

reservas_bp = Blueprint('reservas', __name__)


# ruta para crear una nueva reserva
@reservas_bp.route('/', methods=['POST'])
def create_reserva():
    try:
        data = request.get_json()
        reserva = Reservas(
            created_at=data.get('created_at', datetime.datetime.now()),
            status=data.get('status', 'activa'),
            paquete_id=data['paquete_id'],
            user_id=data['user_id']
        )
        db.session.add(reserva)
        db.session.commit()
        return jsonify({'message': 'Reserva creada correctamente', 'reserva': reserva.id}), 201
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500


# ruta para obtener una reserva por su id
@reservas_bp.route('/<int:id>', methods=['GET'])
def get_reserva(id):
    try:
        reserva = Reservas.query.get(id)
        if reserva is None:
            return jsonify({'message': 'La reserva no fue encontrada'}), 404
        reserva_data = {
            'id': reserva.id,
            'created_at': reserva.created_at,
            'status': reserva.status,
            'paquete_id': reserva.paquete_id,
            'user_id': reserva.user_id,
        }
        return jsonify(reserva_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


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


# ruta para eliminar una reserva
@reservas_bp.route('/<int:id>', methods=['DELETE'])
def delete_reserva(id):
    try:
        reserva = Reservas.query.get(id)
        if reserva is None:
            return jsonify({'message': 'La reserva no fue encontrada'}), 404

        db.session.delete(reserva)
        db.session.commit()
        return jsonify({'message': 'Reserva eliminada correctamente'}), 200
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500
