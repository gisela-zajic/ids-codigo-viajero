# routes/__init__.py

from flask import Blueprint

# importo los blueprints de las diferentes rutas
# backend
from .auth_routes import auth_bp
from .destination_routes import destinos_bp
from .package_routes import paquetes_turisticos_bp
from .reservation_routes import reservas_bp
from .review_routes import resenias_bp
# frontend
from frontend.login.login import auth_front_bp

# creo el blueprint principal
main_bp = Blueprint('main', __name__)

# registro blueprints individuales en el blueprint principal
main_bp.register_blueprint(auth_bp, url_prefix='/auth')
main_bp.register_blueprint(destinos_bp, url_prefix='/destinos')
main_bp.register_blueprint(paquetes_turisticos_bp, url_prefix='/paquetes_turisticos')
main_bp.register_blueprint(reservas_bp, url_prefix='/reservas')
main_bp.register_blueprint(resenias_bp, url_prefix='/resenias')
main_bp.register_blueprint(auth_front_bp, url_prefix='/auth_front')
