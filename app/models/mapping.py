from app.models.base import db
from app.models.entity import Mapping


def get_value(key):
    mapping = Mapping.query.filter(Mapping.key == key).first()
    if mapping:
        return mapping.value
    return None


def set_value(key, value):
    mapping = Mapping.query.filter(Mapping.key == key).first()
    with db.auto_commit():
        if mapping:
            mapping.value = value
        else:
            mapping = Mapping()
            mapping.key = key
            mapping.value = value
            db.session.add(mapping)
