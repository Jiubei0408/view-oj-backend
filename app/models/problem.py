from app.models.base import db
from app.models.entity import Problem


def create_problem(oj_id, problem_pid, rating=0):
    with db.auto_commit():
        r = Problem()
        r.oj_id = oj_id
        r.problem_pid = problem_pid
        r.rating = rating
        db.session.add(r)
    return r


def get_problem_by_problem_info(oj_id, problem_pid, auto_create=True):
    r = Problem.query.filter_by(oj_id=oj_id, problem_pid=problem_pid).first()
    if r:
        return r
    else:
        if auto_create:
            return create_problem(oj_id, problem_pid)


def get_problem_by_problem_id(problem_id):
    return Problem.query.get(problem_id)


def modify_problem_rating(problem_id, rating):
    r = get_problem_by_problem_id(problem_id)
    with db.auto_commit():
        r.rating = rating
