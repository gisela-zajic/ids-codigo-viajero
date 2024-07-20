import datetime
from flask import Blueprint, request, jsonify

from backend.database.models.package import PaquetesTuristicos
from backend.database.models.reservation import Reservas
from backend.database.configs.database import db
from backend.database.models.user import Usuarios

reservas_bp = Blueprint('reservas', __name__)


# ruta para crear una nueva reserva
@reservas_bp.route('/', methods=['POST'])
def create_reserva():
    try:
        data = request.get_json()

        # valido que se envíen los datos necesarios
        if not data or not all(key in data for key in ('paquete_id', 'user_id')):
            return jsonify({'message': 'Faltan datos necesarios'}), 400

        paquete_id = data['paquete_id']
        user_id = data['user_id']

        if not paquete_id or not user_id:
            return jsonify({'message': 'El paquete_id y el user_id son obligatorios'}), 400

        # verifico la existencia del paquete turístico
        paquete = PaquetesTuristicos.query.get(paquete_id)
        if not paquete:
            return jsonify({'message': 'El paquete turístico elegido no existe'}), 404

        # verifico la existencia de usuario
        usuario = Usuarios.query.get(user_id)
        if not usuario:
            return jsonify({'message': 'El usuario elegido no existe'}), 404

        reserva = Reservas(
            created_at=data.get('created_at', datetime.datetime.now()),
            status=data.get('status', 'activa'),
            paquete_id=paquete_id,
            user_id=user_id
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


# ruta para actualizar una reserva
@reservas_bp.route('/<int:id>', methods=['PUT'])
def update_reserva(id):
    try:
        reserva = Reservas.query.get(id)
        if reserva is None:
            return jsonify({'message': 'La reserva no fue encontrada'}), 404

        data = request.get_json()
        reserva.created_at = data.get('created_at', reserva.created_at)
        reserva.status = data.get('status', reserva.status)
        reserva.paquete_id = data.get('paquete_id', reserva.paquete_id)
        reserva.user_id = data.get('user_id', reserva.user_id)

        db.session.commit()
        return jsonify({'message': 'Reserva actualizada correctamente'}), 200
    except Exception as error:
        print('Error', error)
        db.session.rollback()
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
