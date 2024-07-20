import datetime
from flask import Blueprint, request, jsonify
from backend.database.models.review import Resenias
from backend.database.models.package import PaquetesTuristicos
from backend.database.models.user import Usuarios
from backend.database.configs.database import db

resenias_bp = Blueprint('resenias', __name__)


# ruta para crear una nueva reseña
@resenias_bp.route('/', methods=['POST'])
def create_resenia():
    try:
        data = request.get_json()

        # valido que se envíen todos los datos necesarios
        if not data or not all(key in data for key in ('comment', 'rating', 'paquete_id', 'user_id')):
            return jsonify({'message': 'Faltan datos necesarios'}), 400

        comment = data['comment']
        rating = data['rating']
        paquete_id = data['paquete_id']
        user_id = data['user_id']

        # valido que los datos no estén vacíos
        if not comment or not paquete_id or not user_id:
            return jsonify(
                {'message': 'El comentario, la calificación, el id del paquete y el id del user son obligatorios'}), 400
        if rating < 1:
            # valido que la calificación sea al menos 1 punto
            return jsonify({'message': 'La calificación debe ser al menos 1'}), 400

        resenia = Resenias(
            comment=comment,
            created_at=data.get('created_at', datetime.datetime.now()),
            rating=rating,
            paquete_id=paquete_id,
            user_id=user_id
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


#Ruta para obtener todas las reseñas por destino 
@resenias_bp.route("paquete/destino/<int:id_destino>")
def get_resenias_by_destino_id( id_destino):
    try:
        resenias = db.session.query(Resenias.id,Usuarios.username,Resenias.rating,PaquetesTuristicos.name,Resenias.comment,Resenias.created_at
                                    ).join(PaquetesTuristicos,Resenias.paquete_id == PaquetesTuristicos.id
                                    ).join(Usuarios,Resenias.user_id == Usuarios.id
                                    ).filter(PaquetesTuristicos.destino_id == id_destino).all()
        resenias_data = []
        for resenia in resenias:
            resenia_data = {
                'id': resenia[0],
                'user': resenia[1],
                'rating':resenia[2],
                'package': resenia[3],
                'comment':resenia[4],
                'fecha':resenia[5]
            }
            resenias_data.append(resenia_data)
        return jsonify(resenias_data)
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
