import datetime

from sqlalchemy import desc

from app.models.base import db
from app.models.entity import ProblemSet
from app.models.problem_relationship import create_problem_relationship, delete_problem_relationship_by_problem_set_id


def create_problem_set(problem_set_name, problem_list):
    with db.auto_commit():
        r = ProblemSet()
        r.name = problem_set_name
        r.create_time = datetime.datetime.now()
        db.session.add(r)

    for i in problem_list:
        create_problem_relationship(r.id, i)


def modify_problem_set(problem_set_id, problem_set_name, problem_list):
    r = get_problem_set_by_problem_id(problem_set_id)
    with db.auto_commit():
        r.name = problem_set_name

    delete_problem_relationship_by_problem_set_id(problem_set_id)

    for i in problem_list:
        create_problem_relationship(r.id, i)


def delete_problem_set(problem_set_id):
    r = get_problem_set_by_problem_id(problem_set_id)
    if r:
        with db.auto_commit():
            db.session.delete(r)

        delete_problem_relationship_by_problem_set_id(problem_set_id)


def get_problem_set_by_problem_id(problem_set_id):
    return ProblemSet.query.get(problem_set_id)


def get_problem_set_list(page, page_size):
    return [{
        'id': i.id,
        'name': i.name,
        'create_time': i.create_time
    } for i in ProblemSet.query.order_by(desc(ProblemSet.id)).offset((page - 1) * page_size).limit(page_size).all()]
