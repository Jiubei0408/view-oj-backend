from flask import jsonify
from flask_login import login_required

from app.libs.red_print import RedPrint
from app.models.accept_problem import get_accept_problem_list_by_date
from app.models.oj import get_all_oj
from app.validators.forms import InquireForm, RefreshForm

api = RedPrint('data')


@api.route("/get_accept_problem", methods=['POST'])
@login_required
def get_accept_problem_api():
    form = InquireForm().validate_for_api()
    res = get_accept_problem_list_by_date(form.user_id.data, form.start_date.data, form.end_date.data)
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_all_oj", methods=['POST'])
def get_all_oj_api():
    res = get_all_oj()
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/refresh_data", methods=['POST'])
@login_required
def refresh_data_api():
    RefreshForm().validate_for_api()
    pass
