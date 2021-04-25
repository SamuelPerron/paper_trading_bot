from flask import Blueprint, abort

positions_blueprint = Blueprint('positions', __name__)

@positions_blueprint.route('/')
def positions():
    return abort(404)