from flask_sqlalchemy import SQLAlchemy


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgresql@localhost:5434/codigo_viajero'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()
