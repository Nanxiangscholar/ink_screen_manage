from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .auth import *
from .user import *
from .product import *
from .esl import *
from .field import *
from .vue_api import *
