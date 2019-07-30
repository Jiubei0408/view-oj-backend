from app.models.base import db
from app.models.entity import ProblemRelationship


def create_problem_relationship(problem_set_id, problem_id):
    if not ProblemRelationship.query.filter_by(problem_set_id=problem_set_id, problem_id=problem_id).first():
        with db.auto_commit():
            r = ProblemRelationship()
            r.problem_set_id = problem_set_id
            r.problem_id = problem_id
            db.session.add(r)


def delete_problem_relationship_by_problem_set_id(problem_set_id):
    with db.auto_commit():
        ProblemRelationship.query.filter_by(problem_set_id=problem_set_id).delete()
