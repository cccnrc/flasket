from flask import Blueprint

bp = Blueprint('ticket', __name__)

from app.ticket import routes
