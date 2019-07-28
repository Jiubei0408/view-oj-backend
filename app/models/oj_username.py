from app.models.base import db
from app.models.entity import OJUsername


def modify_oj_username(username, oj_id, oj_username):
    r = OJUsername.query.filter_by(username=username, oj_id=oj_id).first()
    if not r and oj_username:
        add_oj_username(username, oj_id, oj_username)
    else:
        with db.auto_commit():
            if oj_username:
                r.oj_username = oj_username
            else:
                db.session.delete(r)


def add_oj_username(username, oj_id, oj_username):
    with db.auto_commit():
        r = OJUsername()
        r.username = username
        r.oj_id = oj_id
        r.oj_username = oj_username
        db.session.add(r)


def get_oj_username(username, oj_id):
    r = OJUsername.query.filter_by(username=username, oj_id=oj_id).first()
    if r:
        return r.oj_username


def get_user_oj_username(username):
    return [{
        'oj_id': i.oj_id,
        'oj_name': i.oj.name,
        'oj_username': i.oj_username
    } for i in OJUsername.query.filter_by(username=username).all()]


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = get_oj_username(3, 1)
    print(r)
