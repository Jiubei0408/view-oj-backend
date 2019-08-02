from app.config.setting import DEFAULT_USER_RATING
from app.models.accept_problem import get_accept_problem_list_by_username, modify_accept_problem_add_rating


def calculate_problem_rating(total, accept):
    accept_rate = accept / total

    if accept >= 30000:
        return 800
    if accept_rate > 0.6:
        return 800
    if accept_rate > 0.4:
        return 1200
    if accept_rate > 0.3:
        return 1600
    if accept_rate > 0.2:
        return 2000
    if accept_rate > 0.1:
        return 2400
    return 3000


def calculate_user_add_rating(user_rating, problem_rating):
    return int((problem_rating / user_rating) ** 2 * 5)


def calculate_user_rating(username):
    user_rating = DEFAULT_USER_RATING
    for problem in get_accept_problem_list_by_username(username):
        add_rating = calculate_user_add_rating(user_rating, problem.problem.rating)
        modify_accept_problem_add_rating(problem.id, add_rating)
        user_rating += add_rating
