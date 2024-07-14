from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.user import Usuarios
from app.models.destination import Destinos
from app.models.package import PaquetesTuristicos
from app.models.reservation import Reservas
from app.models.review import Resenias
