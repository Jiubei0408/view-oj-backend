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


def calculate_user_rating(user_rating, problem_rating):
    return int((problem_rating ** 2) / (user_rating ** 2) * 10)
