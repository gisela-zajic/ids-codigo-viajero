import datetime
from flask import Blueprint, request, jsonify
from app.models.user import Usuarios
from app import db

auth_bp = Blueprint('auth', __name__)


# ruta para registro de usuario
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        created_at = data.get('created_at', datetime.datetime.now())
        usuario = Usuarios(username=username, email=email, password=password, created_at=created_at)
        db.session.add(usuario)
        db.session.commit()
        return jsonify({'message': f'Usuario creado correctamente como: {username}'}), 201
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500


# ruta para obtener un usuario por su id
@auth_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    try:
        usuario = Usuarios.query.get(id)
        if usuario is None:
            return jsonify({'message': 'El usuario no fue encontrado'}), 404
        usuario_data = {
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'created_at': usuario.created_at
        }
        return jsonify({'user': usuario_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


# ruta para iniciar sesión
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        usuario = Usuarios.query.filter_by(email=email).first()
        if usuario and usuario.password == password:
            return jsonify({'message': f'Bienvenido, {usuario.username}!'}), 200
        return jsonify({'message': 'Credenciales incorrectas'}), 401
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


# ruta para eliminar un usuario
@auth_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        usuario = Usuarios.query.get(id)
        if usuario is None:
            return jsonify({'message': 'El usuario no fue encontrado'}), 404

        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado correctamente'}), 200
    except Exception as error:
        print('Error', error)
        db.session.rollback()
        return jsonify({'message': 'Internal server error'}), 500
