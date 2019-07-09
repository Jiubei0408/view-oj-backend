from flask import jsonify

from app.libs.red_print import RedPrint
from app.models.accept import get_accept_list_by_date
from app.validators.forms import InquireForm

api = RedPrint('data')


@api.route("/get_accept_problem", methods=['POST'])
def get_accept_problem_api():
    form = InquireForm().validate_for_api()
    res = get_accept_list_by_date(form.user_id.data, form.start_date.data, form.end_date.data)
    return jsonify(res)
