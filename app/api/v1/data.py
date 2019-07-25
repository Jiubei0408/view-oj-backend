from flask import jsonify
from flask_login import login_required, current_user

from app.libs.error_code import Success, Forbidden
from app.libs.red_print import RedPrint
from app.models.accept_problem import get_accept_problem_list_by_date, get_accept_problem_count_by_date, \
    get_accept_problem_distributed
from app.models.oj import get_all_oj
from app.models.task import task_is_exist
from app.models.user import get_all_user
from app.spiders.oj_spider import task_crawl_oj_info
from app.validators.forms import DateForm, UserIdForm, InquireForm, RefreshForm

api = RedPrint('data')


@api.route("/get_all_oj_info", methods=['POST'])
def get_all_oj_info_api():
    res = get_all_oj()
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_accept_problem", methods=['POST'])
@login_required
def get_accept_problem_api():
    form = InquireForm().validate_for_api()
    res = get_accept_problem_list_by_date(form.user_id.data, form.start_date.data, form.end_date.data)
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_accept_problem_distributed", methods=['POST'])
@login_required
def get_accept_problem_distributed_api():
    form = UserIdForm().validate_for_api()
    res = get_accept_problem_distributed(form.user_id.data)
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_all_accept_problem_count", methods=['POST'])
@login_required
def get_all_accept_problem_count_api():
    form = DateForm().validate_for_api()
    res = list()
    for user in get_all_user():
        res.append({
            'id': user['id'],
            'username': user['username'],
            'nickname': user['nickname'],
            'accept_problem_count': get_accept_problem_count_by_date(user['id'], form.start_date.data,
                                                                     form.end_date.data)
        })
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/refresh_data", methods=['POST'])
@login_required
def refresh_data_api():
    form = RefreshForm().validate_for_api()
    if task_is_exist(form.user_id.data, form.oj_id.data):
        return Forbidden('The mission is not over yet, please do not submit again')
    task_crawl_oj_info(form.user_id.data, form.oj_id.data)
    return Success('Submit refresh request successfully')


@api.route("/refresh_all_data", methods=['POST'])
@login_required
def refresh_all_data_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    for user in get_all_user():
        for oj in get_all_oj():
            if oj['status'] and user['status'] and not task_is_exist(user['id'], oj['id']):
                task_crawl_oj_info(user['id'], oj['id'])
    return Success('Submit all refresh request successfully')
