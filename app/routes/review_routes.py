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
