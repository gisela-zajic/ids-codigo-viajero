from flask import Flask, request, jsonify
from models import db, Destinos, Paquetes_turisticos, Resenias, Reservas, Usuarios

app =Flask(__name__)
port = 5432
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2-binary://postgres:postgresql@localhost:5432/codigo_viajero'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS']=False

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = Usuarios.query.all()
        usuarios_data = []
        for usuario in usuarios:
            usuario_data = {
                'id': usuario.id,
                'username' : usuario.username,
                'email' : usuario.email,
                'password' : usuario.password,
                'created_at' : usuario.created_at
            }
            usuarios_data.append(usuario_data)
        return jsonify({'usuarios': usuarios_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500 
            
@app.route('/destinos', methods=['GET'])
def get_destinos():
    try:
        destinos = Destinos.query.all()
        destinos_data = []
        for destino in destinos:
            destino_data = {
                'id': destino.id,
                'name' : destino.name,
                'description' : destino.description,
                'location' : destino.location,
                'image_url' : destino.image_url,
                'created_at' : destino.created_at
            }
            destinos_data.append(destino_data)
        return jsonify({'destinos': destino_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/paquetes_turiticos', methods=['GET'])
def get_paquetes_turisticos():
    try:
        paquetes_turisticos = Paquetes_turisticos.query.all()
        paquetes_turisticos_data = []
        for paquete_turistico in paquetes_turisticos:
            paquete_turistico_data = {
                'id': paquete_turistico.id,
                'paquetes_turiticos_id' : paquete_turistico.paquetes_turiticos_id,
                'name' : paquete_turistico.name,
                'description' : paquete_turistico.description,
                'price' : paquete_turistico.price,
                'image_url' : paquete_turistico.image_url,
                'created_at' : paquete_turistico.created_at
            }
            paquetes_turisticos_data.append(paquete_turistico_data)
        return jsonify({'paquetes_turiticos': paquete_turistico})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/resenias', methods=['GET'])
def get_resenias():
    try:
        resenias = Resenias.query.all()
        resenias_data = []
        for resenia in resenias:
            resenia_data = {
                'id': resenia.id,
                'comment' : resenia.comment,
                'created_at' : resenia.created_at,
                'rating' : resenia.rating,
                'paquetes_id' : resenia.paquetes_id,
                'user_id' : resenia.user_id,
            }
            resenias_data.append(resenia_data)
        return jsonify({'resenias': resenia})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/reservas', methods=['GET'])
def get_reservas():
    try:
        reservas = Reservas.query.all()
        reservas_data = []
        for reserva in reservas:
            reserva_data = {
                'id': reserva.id,
                'created_at' : reserva.created_at,
                'status' : reserva.status,
                'paquetes_id' : reserva.paquetes_id,
                'user_id' : reserva.user_id,
            }
            reservas_data.append(reserva_data)
        return jsonify({'reservas': reserva})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500



if __name__ == '__main__':
    print('Starting server')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print('Started...')
    app.run(host='0.0.0.0', debug=True, port=port)