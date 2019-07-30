from flask import jsonify
from flask_login import login_required, current_user

from app.libs.error_code import Success, Forbidden
from app.libs.red_print import RedPrint
from app.models.oj import get_oj_list
from app.models.task import create_task, get_task, get_task_count
from app.models.user import get_user_list
from app.validators.forms import RefreshAcceptProblemForm, RefreshProblemRatingForm

api = RedPrint('task')


@api.route("/refresh_all_data", methods=['POST'])
@login_required
def refresh_all_data_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    for user in get_user_list():
        for oj in get_oj_list():
            if oj['status'] and user['status']:
                task = get_task('crawl_accept_problem', {
                    'username': user['username'],
                    'oj_id': oj['id']
                })
                if not task or task.status != 2:
                    create_task('crawl_accept_problem', {
                        'username': user['username'],
                        'oj_id': oj['id']
                    })
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
    return Success('Submit refresh request successfully')


@api.route("/get_task_count", methods=['POST'])
@login_required
def get_task_count_api():
    res = get_task_count()
    return jsonify({
        'code': 0,
        'data': res
    })
