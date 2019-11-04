from app.config.setting import DEFAULT_USER_RATING
from app.models.accept_problem import get_accept_problem_list_by_username, modify_accept_problem_add_rating
import xgboost as xgb

xgb_model = xgb.XGBRegressor()
try:
    xgb_model.load_model('rating.model')
except:
    xgb_model.load_model('../../rating.model')


def calculate_problem_rating(total, accept):
    accept_rate = accept / total

    try:
        predict_rating = int(xgb_model.predict([accept, total, accept_rate])[0])
    except:
        predict_rating = -9999999

    if accept >= 30000:
        rating = 800
    elif accept_rate > 0.6:
        rating = 800
    elif accept_rate > 0.4:
        rating = 1200
    elif accept_rate > 0.3:
        rating = 1600
    elif accept_rate > 0.2:
        rating = 2000
    elif accept_rate > 0.1:
        rating = 2400
    else:
        rating = 3000

    if abs(rating - predict_rating) < 1000:
        return predict_rating
    return rating


def calculate_user_add_rating(user_rating, problem_rating):
    return int((problem_rating / user_rating) ** 2 * 5)


def calculate_user_rating(username):
    user_rating = DEFAULT_USER_RATING
    for problem in get_accept_problem_list_by_username(username):
        add_rating = calculate_user_add_rating(user_rating, problem.problem.rating)
        modify_accept_problem_add_rating(problem.id, add_rating)
        user_rating += add_rating


if __name__ == '__main__':
    a = calculate_problem_rating(1, 1)
    print(a)
