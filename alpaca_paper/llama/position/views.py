from flask import Blueprint, abort
from .. import app
# from .models import Account

positions_blueprint = Blueprint('positions', __name__)

@positions_blueprint.route('/')
def positions():
    return abort(404)