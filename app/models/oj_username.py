import datetime

from app.models.base import db
from app.models.entity import OJUsername
from app.models.oj import get_oj_list


def modify_oj_username(username, oj_id, oj_username, oj_password, oj_cookies=None):
    r = OJUsername.query.filter_by(username=username, oj_id=oj_id).first()
    if not r and oj_username:
        create_oj_username(username, oj_id, oj_username, oj_password)
    else:
        if r:
            with db.auto_commit():
                if oj_username:
                    r.oj_username = oj_username
                    r.oj_password = oj_password
                    r.oj_cookies = oj_cookies
                else:
                    db.session.delete(r)


def update_success_time(username, oj_id):
    r = OJUsername.query.filter_by(username=username, oj_id=oj_id).first()
    with db.auto_commit():
        r.last_success_time = datetime.datetime.now()


def create_oj_username(username, oj_id, oj_username, oj_password):
    with db.auto_commit():
        r = OJUsername()
        r.username = username
        r.oj_id = oj_id
        r.oj_username = oj_username
        r.oj_password = oj_password
        db.session.add(r)


def get_oj_username(username, oj_id):
    return OJUsername.query.filter_by(username=username, oj_id=oj_id).first()


def get_user_oj_username(username):
    oj_list = get_oj_list()
    r = list()
    for i in oj_list:
        if i['status']:
            oj_username = OJUsername.query.filter_by(username=username, oj_id=i['id']).first()
            if oj_username is None:
                last_success_time = None
                oj_username = ""
            else:
                last_success_time = oj_username.last_success_time
                oj_username = oj_username.oj_username

            r.append({
                'oj_id': i['id'],
                'oj_name': i['name'],
                'oj_username': oj_username,
                'last_success_time': last_success_time
            })
    return r


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = get_oj_username(3, 1)
    print(r)
