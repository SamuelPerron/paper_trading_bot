from flask import Blueprint, abort
from .. import app

orders_blueprint = Blueprint('orders', __name__)

@orders_blueprint.route('/')
def orders():
    return abort(404)