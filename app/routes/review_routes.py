import datetime
from flask import Blueprint, request, jsonify
from app.models.review import Resenias
from app import db

resenias_bp = Blueprint('resenias', __name__)


# ruta para crear una nueva reseña
@resenias_bp.route('/', methods=['POST'])
def create_resenia():
    try:
        data = request.get_json()
        resenia = Resenias(
            comment=data['comment'],
            created_at=data.get('created_at', datetime.datetime.now()),
            rating=data['rating'],
            paquete_id=data['paquete_id'],
            user_id=data['user_id']
        )
        db.session.add(resenia)
        db.session.commit()
        return jsonify({'message': 'Reseña creada correctamente', 'resenia': resenia.id}), 201
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500


# ruta para obtener una reseña por su id
@resenias_bp.route('/<int:id>', methods=['GET'])
def get_resenia(id):
    try:
        resenia = Resenias.query.get(id)
        if resenia is None:
            return jsonify({'message': 'La reseña no fue encontrada'}), 404
        resenia_data = {
            'id': resenia.id,
            'comment': resenia.comment,
            'created_at': resenia.created_at,
            'rating': resenia.rating,
            'paquete_id': resenia.paquete_id,
            'user_id': resenia.user_id,
        }
        return jsonify(resenia_data)
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


# ruta para actualizar una reseña
@resenias_bp.route('/<int:id>', methods=['PUT'])
def update_resenia(id):
    try:
        resenia = Resenias.query.get(id)
        if resenia is None:
            return jsonify({'message': 'La reseña no fue encontrada'}), 404

        data = request.get_json()
        resenia.comment = data.get('comment', resenia.comment)
        resenia.created_at = data.get('created_at', resenia.created_at)
        resenia.rating = data.get('rating', resenia.rating)
        resenia.paquete_id = data.get('paquete_id', resenia.paquete_id)
        resenia.user_id = data.get('user_id', resenia.user_id)

        db.session.commit()
        return jsonify({'message': 'Reseña actualizada correctamente'}), 200
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500


# ruta para obtener todas las reseñas
@resenias_bp.route('/', methods=['GET'])
def get_resenias():
    try:
        resenias = Resenias.query.all()
        resenias_data = []
        for resenia in resenias:
            resenia_data = {
                'id': resenia.id,
                'comment': resenia.comment,
                'created_at': resenia.created_at,
                'rating': resenia.rating,
                'paquete_id': resenia.paquete_id,
                'user_id': resenia.user_id,
            }
            resenias_data.append(resenia_data)
        return jsonify({'resenias': resenias_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


# ruta para eliminar una reseña
@resenias_bp.route('/<int:id>', methods=['DELETE'])
def delete_resenia(id):
    try:
        resenia = Resenias.query.get(id)
        if resenia is None:
            return jsonify({'message': 'La reseña no fue encontrada'}), 404

        db.session.delete(resenia)
        db.session.commit()
        return jsonify({'message': 'Reseña eliminada correctamente'}), 200
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500
