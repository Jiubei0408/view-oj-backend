from flask_login import login_required, current_user

from app.libs.error_code import Success, Forbidden
from app.libs.red_print import RedPrint
from app.models.oj import get_all_oj
from app.models.task import create_task, get_task
from app.models.user import get_all_user
from app.validators.forms import RefreshForm

api = RedPrint('task')


@api.route("/refresh_data", methods=['POST'])
@login_required
def refresh_data_api():
    form = RefreshForm().validate_for_api()
    task = get_task('crawl_accept_problem', {
        'username': form.username.data,
        'oj_id': form.oj_id.data
    })
    if not task or task.status != 2:
        return Forbidden('The mission is not over yet, please do not submit again')
    create_task('crawl_accept_problem', {
        'username': form.username.data,
        'oj_id': form.oj_id.data
    })
    return Success('Submit refresh request successfully')


@api.route("/refresh_all_data", methods=['POST'])
@login_required
def refresh_all_data_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    for user in get_all_user():
        for oj in get_all_oj():
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
