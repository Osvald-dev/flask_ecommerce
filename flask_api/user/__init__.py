from flask import Blueprint
from .user_routes import user_bp
from .user_model import User
from .user_dao import UsuarioDAO
from flask_api.db import db

user_bp = Blueprint ('user', __name__, url_prefix='/api/user')

from . import user_routes