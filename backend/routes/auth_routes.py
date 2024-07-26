import datetime
from flask import Blueprint, request, jsonify

from backend.database.configs.database import db
from backend.database.models.user import Usuarios

auth_bp = Blueprint('auth', __name__)


# ruta para registro de usuario
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ('username', 'email', 'password')):
            return jsonify({'message': 'Faltan datos necesarios'}), 400

        username = data['username']
        email = data['email']
        password = data['password']
        if not username or not email or not password:
            return jsonify({'message': 'Todos los campos son obligatorios'}), 400

        if len(password) < 6:
            return jsonify({'message': 'La contraseña debe tener al menos 6 caracteres'}), 400

        created_at = data.get('created_at', datetime.datetime.now())
        usuario = Usuarios(username=username, email=email, password=password, created_at=created_at)
        if Usuarios.query.filter((Usuarios.username == username) | (Usuarios.email == email)).first():
            return jsonify({'message': 'El nombre de usuario o el correo electrónico ya existen'}), 400

        db.session.add(usuario)
        db.session.commit()
        return jsonify({'message': f'Usuario creado correctamente como: {username}'}), 201
    except Exception as error:
        print('Error', error)
        db.session.rollback()
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
            return jsonify({'message': f'Bienvenido, {usuario.username}!', 'user_id': usuario.id}), 200
        return jsonify({'message': 'Credenciales incorrectas'}), 401
    except Exception as error:
        print('Error', error)
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


# ruta para actualizar la información del usuario
@auth_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        usuario = Usuarios.query.get(id)
        if usuario is None:
            return jsonify({'message': 'El usuario no fue encontrado'}), 404

        data = request.get_json()
        usuario.username = data.get('username', usuario.username)
        usuario.email = data.get('email', usuario.email)
        usuario.password = data.get('password', usuario.password)

        db.session.commit()
        return jsonify({'message': 'Información del usuario actualizada correctamente'}), 200
    except Exception as error:
        print('Error', error)
        db.session.rollback()
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
