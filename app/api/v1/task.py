from flask import jsonify
from flask_login import login_required, current_user

from app.libs.error_code import Success, Forbidden
from app.libs.red_print import RedPrint
from app.models.oj import get_all_oj
from app.models.task import task_is_exist, create_task, get_all_task
from app.models.user import get_all_user
from app.validators.forms import RefreshForm

api = RedPrint('task')


@api.route("/refresh_data", methods=['POST'])
@login_required
def refresh_data_api():
    form = RefreshForm().validate_for_api()
    if task_is_exist(form.user_id.data, form.oj_id.data):
        return Forbidden('The mission is not over yet, please do not submit again')
    create_task(form.user_id.data, form.oj_id.data)
    return Success('Submit refresh request successfully')


@api.route("/refresh_all_data", methods=['POST'])
@login_required
def refresh_all_data_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    for user in get_all_user():
        for oj in get_all_oj():
            if oj['status'] and user['status'] and not task_is_exist(user['id'], oj['id']):
                create_task(user['id'], oj['id'])
    return Success('Submit all refresh request successfully')


@api.route("/get_task_list", methods=['POST'])
@login_required
def get_task_list():
    res = get_all_task()
    return jsonify({
        'code': 0,
        'data': res
    })
