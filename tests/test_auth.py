import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


# prueba de registro exitoso
def test_register_200(client):
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Usuario creado correctamente como: testuser'


# prueba de registro con campos faltantes
def test_register_missing_fields(client):
    response = client.post('/auth/register', json={
        'username': 'testuser'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Faltan datos necesarios'


# prueba de registro con contraseña corta
def test_register_short_password(client):
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': '123'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'La contraseña debe tener al menos 6 caracteres'
