import datetime
import json

from app.models.base import db
from app.models.entity import Task


def create_task(task_name, kwargs):
    with db.auto_commit():
        task = Task()
        task.task_name = task_name
        task.kwargs = json.dumps(kwargs)
        task.status = 0
        task.create_time = datetime.datetime.now()
        db.session.add(task)


def get_an_idle_task():
    return Task.query.filter_by(status=0).order_by(Task.id).first()


def start_task(task_id):
    task = Task.query.get(task_id)
    with db.auto_commit():
        task.status = 1
        task.start_time = datetime.datetime.now()


def finish_task(task_id):
    task = Task.query.get(task_id)
    with db.auto_commit():
        task.status = 2
        task.finish_time = datetime.datetime.now()


def get_task(task_name, kwargs):
    return Task.query.filter_by(task_name=task_name, kwargs=json.dumps(kwargs), status=0).first()


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = finish_task(1, 2)
    print(r)
