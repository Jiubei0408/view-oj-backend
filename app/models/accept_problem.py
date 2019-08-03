import datetime

from sqlalchemy import func, desc, asc

from app.config.setting import DEFAULT_USER_RATING
from app.models.base import db
from app.models.entity import AcceptProblem, Problem, User


def create_accept_problem(username, problem_id, add_rating):
    if not AcceptProblem.query.filter_by(username=username, problem_id=problem_id).first():
        with db.auto_commit():
            r = AcceptProblem()
            r.username = username
            r.problem_id = problem_id
            r.add_rating = add_rating
            r.create_time = datetime.datetime.now()
            db.session.add(r)


def get_accept_problem_list_by_username(username):
    return AcceptProblem.query.filter_by(username=username).order_by(asc(AcceptProblem.id)).all()


def get_accept_problem_list_by_oj_id(username, oj_id):
    return [i.problem_pid for i in Problem.query.filter(
        Problem.oj_id == oj_id,
        Problem.id.in_(db.session.query(AcceptProblem.problem_id).filter_by(username=username).subquery())
    ).all()]


def get_accept_problem_list_by_date(username, start_date, end_date, page, page_size):
    return {
        'count': AcceptProblem.query.filter(
            AcceptProblem.username == username,
            AcceptProblem.create_time >= start_date,
            AcceptProblem.create_time <= end_date
        ).count(),
        'data': [{
            'oj_id': i.problem.oj_id,
            'oj_name': i.problem.oj.name,
            'problem_id': i.problem_id,
            'problem_pid': i.problem.problem_pid,
            'rating': i.problem.rating,
            'add_rating': i.add_rating,
            'create_time': i.create_time
        } for i in AcceptProblem.query.filter(
            AcceptProblem.username == username,
            AcceptProblem.create_time >= start_date,
            AcceptProblem.create_time < end_date
        ).order_by(desc(AcceptProblem.create_time)).offset((page - 1) * page_size).limit(page_size).all()]
    }


def get_accept_problem_count_by_date(username, start_date, end_date):
    return AcceptProblem.query.filter(
        AcceptProblem.username == username,
        AcceptProblem.create_time >= start_date,
        AcceptProblem.create_time <= end_date
    ).count()


def get_accept_problem_date_distributed(username, start_date, end_date):
    r = list()
    now_date = start_date
    while now_date != end_date:
        r.append({
            'date': now_date,
            'count': AcceptProblem.query.filter(
                AcceptProblem.username == username,
                AcceptProblem.create_time >= now_date,
                AcceptProblem.create_time < now_date + datetime.timedelta(days=1)
            ).count()
        })
        now_date = now_date + datetime.timedelta(days=1)
    return r


def get_accept_problem_oj_distributed(username):
    return [{
        'oj_id': i[0].oj_id,
        'oj_name': i[0].oj.name,
        'accept_problem_count': i[1]
    } for i in
        db.session.query(Problem, func.count(Problem.id)).join(AcceptProblem).filter(
            AcceptProblem.username == username
        ).group_by(Problem.oj_id).all()]


def get_accept_problem_by_problem_id(problem_id):
    return AcceptProblem.query.filter_by(problem_id=problem_id).all()


def delete_accept_problem_by_oj_id(username, oj_id):
    with db.auto_commit():
        AcceptProblem.query.filter(
            AcceptProblem.username == username,
            AcceptProblem.problem_id.in_(db.session.query(Problem.id).filter_by(oj_id=oj_id).subquery())
        ).delete(synchronize_session='fetch')


def get_rating_by_username(username):
    add_rating = db.session.query(func.sum(AcceptProblem.add_rating)).filter(
        AcceptProblem.username == username
    ).first()[0]
    if add_rating is None:
        add_rating = 0
    return DEFAULT_USER_RATING + int(add_rating)


def get_rating_rank_list():
    return [{
        'username': i[0],
        'nickname': i[1],
        'rating': DEFAULT_USER_RATING + int(i[2])
    } for i in db.session.query(
        User.username, User.nickname, func.sum(AcceptProblem.add_rating)).filter(
        User.username == AcceptProblem.username,
        User.status == 1
    ).group_by(User.username).order_by(desc(func.sum(AcceptProblem.add_rating))).all()]


def get_accept_problem_by_username_problem_id(username, problem_id):
    return AcceptProblem.query.filter_by(username=username, problem_id=problem_id).first()


def get_accept_problem_by_problem_list(username, problem_list):
    return AcceptProblem.query.join(Problem).filter(Problem.id.in_(problem_list),
                                                    AcceptProblem.username == username).all()


def modify_accept_problem_add_rating(accept_problem_id, add_rating):
    r = AcceptProblem.query.get(accept_problem_id)
    with db.auto_commit():
        r.add_rating = add_rating


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        s = datetime.date.today()
        e = datetime.date.today() + datetime.timedelta(days=1)
        r = get_rating_rank_list()
    print(r)
