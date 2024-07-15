from flask import Blueprint, request, jsonify
from app.models.review import Resenias
from app import db

resenias_bp = Blueprint('resenias', __name__)


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
