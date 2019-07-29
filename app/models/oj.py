from app.models.base import db
from app.models.entity import OJ


def get_oj_by_oj_id(oj_id):
    return OJ.query.get(oj_id)


def get_oj_list():
    return [{
        'id': i.id,
        'name': i.name,
        'status': i.status
    } for i in OJ.query.all()]


def add_oj(oj_name):
    with db.auto_commit():
        oj = OJ()
        oj.name = oj_name
        oj.status = 0
        db.session.add(oj)
    return oj


def get_oj_by_oj_name(oj_name):
    oj = OJ.query.filter_by(name=oj_name).first()
    if oj:
        return oj
    else:
        return add_oj(oj_name)


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = get_oj_by_oj_id(1)
    print(r)
