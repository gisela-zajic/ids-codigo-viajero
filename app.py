from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from backend.database.configs.database import db
from backend.routes.register import register_routes

PORT = 5433


def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.database.configs.database.Config')

    db.init_app(app)
    Migrate(app, db)

    register_routes(app)
    CORS(app)
    return app


if __name__ == '__main__':
    print('Starting server...')
    app = create_app()
    with app.app_context():
        db.create_all()
    print('Started...')
    app.run(debug=True, port=PORT)
