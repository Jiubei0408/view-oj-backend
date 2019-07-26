from flask import jsonify
from flask_login import login_required
from app.libs.red_print import RedPrint
from app.models.accept_problem import get_accept_problem_list_by_date, get_accept_problem_count_by_date, \
    get_accept_problem_distributed
from app.models.oj import get_all_oj
from app.models.user import get_all_user
from app.validators.forms import DateForm, UserIdForm, InquireForm

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
def get_all_accept_problem_count_api():
    form = DateForm().validate_for_api()
    res = list()
    for user in get_all_user():
        if user['status']:
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
