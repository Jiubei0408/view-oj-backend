from flask import Blueprint

from app.api.v1 import data, user, task


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    user.api.register(bp_v1)
    data.api.register(bp_v1)
    task.api.register(bp_v1)
    return bp_v1
