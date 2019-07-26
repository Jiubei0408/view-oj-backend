import datetime

from sqlalchemy import Column, Integer, DateTime, desc

from app.models.base import Base, db


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    oj_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False)
    finish_time = Column(DateTime)


def create_task(user_id, oj_id):
    with db.auto_commit():
        task = Task()
        task.user_id = user_id
        task.oj_id = oj_id
        task.status = 0
        task.create_time = datetime.datetime.now()
        db.session.add(task)


def get_task():
    return Task.query.filter_by(status=0).order_by(Task.id).first()


def finish_task(task_id):
    task = Task.query.get(task_id)
    with db.auto_commit():
        task.status = 1
        task.finish_time = datetime.datetime.now()


def task_is_exist(user_id, oj_id):
    return Task.query.filter_by(user_id=user_id, oj_id=oj_id, status=0).order_by(Task.id).first() is not None


def get_all_task():
    r = Task.query.order_by(desc(Task.id)).all()
    rr = []
    for i in r:
        rr.append({
            'id': i.id,
            'user_id': i.user_id,
            'oj_id': i.oj_id,
            'create_time': i.create_time,
            'finish_time': i.finish_time
        })
    return rr


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = finish_task(1, 2)
    print(r)
