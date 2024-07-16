from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder="frontend")
    app.config.from_object('backend.app.config.Config')

    db.init_app(app)
    Migrate(app, db)

    # importo y registro el blueprint principal
    from backend.app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
