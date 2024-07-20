from flask import Blueprint
from backend.routes.auth_routes import auth_bp
from backend.routes.destination_routes import destinos_bp
from backend.routes.package_routes import paquetes_turisticos_bp
from backend.routes.reservation_routes import reservas_bp
from backend.routes.review_routes import resenias_bp
from frontend.handler.login import auth_front


def register_routes(app):
    # creo el blueprint principal
    main_bp = Blueprint('main', __name__)

    # registro blueprints individuales en el blueprint principal
    main_bp.register_blueprint(auth_bp, url_prefix='/auth')
    main_bp.register_blueprint(destinos_bp, url_prefix='/destinos')
    main_bp.register_blueprint(paquetes_turisticos_bp, url_prefix='/paquetes_turisticos')
    main_bp.register_blueprint(reservas_bp, url_prefix='/reservas')
    main_bp.register_blueprint(resenias_bp, url_prefix='/resenias')

    main_bp.register_blueprint(auth_front, url_prefix='/')
    app.register_blueprint(main_bp)

    return app
