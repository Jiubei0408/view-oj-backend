import datetime

from sqlalchemy import Column, Integer, String, DateTime

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


def get_task(user_id, oj_id):
    return Task.query.filter_by(user_id=user_id, oj_id=oj_id, status=0).first()


def finish_task(user_id, oj_id):
    task = get_task(user_id, oj_id)
    if task:
        with db.auto_commit():
            task.status = 1
            task.finish_time = datetime.datetime.now()


def task_is_exist(user_id, oj_id):
    return get_task(user_id, oj_id) is not None


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = finish_task(1, 2)
    print(r)
