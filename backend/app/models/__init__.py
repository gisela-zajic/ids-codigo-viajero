from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from backend.app.models.user import Usuarios
from backend.app.models.destination import Destinos
from backend.app.models.package import PaquetesTuristicos
from backend.app.models.reservation import Reservas
from backend.app.models.review import Resenias
