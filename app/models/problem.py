from app.models.base import db
from app.models.entity import Problem


def create_problem(oj_id, problem_pid, rating=1500):
    with db.auto_commit():
        r = Problem()
        r.oj_id = oj_id
        r.problem_pid = problem_pid
        r.rating = rating
        db.session.add(r)
    return r
