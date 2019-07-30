from app.models.base import db
from app.models.entity import OJUsername
from app.models.oj import get_oj_list


def modify_oj_username(username, oj_id, oj_username):
    r = OJUsername.query.filter_by(username=username, oj_id=oj_id).first()
    if not r and oj_username:
        create_oj_username(username, oj_id, oj_username)
    else:
        with db.auto_commit():
            if oj_username:
                r.oj_username = oj_username
            else:
                db.session.delete(r)


def create_oj_username(username, oj_id, oj_username):
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
    oj_list = get_oj_list()
    r = list()
    for i in oj_list:
        if i['status']:
            oj_username = OJUsername.query.filter_by(username=username, oj_id=i['id']).first()
            if oj_username is None:
                oj_username = ""
            else:
                oj_username = oj_username.oj_username
            r.append({
                'oj_id': i['id'],
                'oj_name': i['name'],
                'oj_username': oj_username
            })
    return r


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = get_oj_username(3, 1)
    print(r)
