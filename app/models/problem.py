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


def get_problem(oj_id, problem_pid):
    r = Problem.query.filter_by(oj_id=oj_id, problem_pid=problem_pid).first()
    if r:
        return r
    else:
        return create_problem(oj_id, problem_pid)
