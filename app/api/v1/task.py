from flask import jsonify
from flask_login import login_required, current_user

from app.libs.error_code import Success, Forbidden
from app.libs.red_print import RedPrint
from app.models.problem_set import get_problem_set_by_problem_id
from app.models.task import create_task, get_task, get_task_count
from app.models.user import get_user_list
from app.validators.forms import RefreshAcceptProblemForm, RefreshProblemRatingForm, ProblemSetIdForm, \
    NoAuthUsernameForm
from tasks import task_crawl_all_accept_problem, task_crawl_accept_problem, task_crawl_problem_rating, \
    task_calculate_user_rating

api = RedPrint('task')


@api.route("/get_task_count", methods=['POST'])
def get_task_count_api():
    res = get_task_count()
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/refresh_all_data", methods=['POST'])
@login_required
def refresh_all_data_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    task_crawl_all_accept_problem.delay()
    return Success('Submit all refresh request successfully')


@api.route("/refresh_accept_problem", methods=['POST'])
@login_required
def refresh_accept_problem_api():
    form = RefreshAcceptProblemForm().validate_for_api()
    task = get_task('crawl_accept_problem', {
        'username': form.username.data,
        'oj_id': form.oj_id.data
    })
    if task and task.status != 2:
        return Forbidden('The mission is not over yet, please do not submit again')
    create_task('crawl_accept_problem', {
        'username': form.username.data,
        'oj_id': form.oj_id.data
    })
    task_crawl_accept_problem.delay(form.username.data, form.oj_id.data)
    return Success('Submit refresh request successfully')


@api.route("/refresh_problem_rating", methods=['POST'])
@login_required
def refresh_problem_rating_api():
    form = RefreshProblemRatingForm().validate_for_api()
    task = get_task('crawl_problem_rating', {
        'problem_id': form.problem_id.data,
    })
    if task and task.status != 2:
        return Forbidden('The mission is not over yet, please do not submit again')
    create_task('crawl_problem_rating', {
        'problem_id': form.problem_id.data,
    })
    task_crawl_problem_rating.delay(form.problem_id.data)
    return Success('Submit refresh request successfully')


@api.route("/refresh_problem_set", methods=['POST'])
def refresh_problem_set_api():
    form = ProblemSetIdForm().validate_for_api()
    problem_set = get_problem_set_by_problem_id(form.problem_set_id.data)
    for problem in problem_set.problem:
        for user in get_user_list():
            task = get_task('crawl_accept_problem', {
                'username': user['username'],
                'oj_id': problem.problem.oj_id
            })
            if not task or task.status == 2:
                create_task('crawl_accept_problem', {
                    'username': user['username'],
                    'oj_id': problem.problem.oj_id
                })
                task_crawl_accept_problem.delay(user['username'], problem.problem.oj_id)
    return Success('Submit refresh request successfully')


@api.route("/refresh_user_rating", methods=['POST'])
def refresh_user_rating_api():
    form = NoAuthUsernameForm().validate_for_api()
    task = get_task('calculate_user_rating', {
        'username': form.username.data,
    })
    if task and task.status != 2:
        return Forbidden('The mission is not over yet, please do not submit again')
    create_task('calculate_user_rating', {
        'username': form.username.data,
    })
    task_calculate_user_rating.delay(form.username.data)
    return Success('Submit refresh request successfully')
