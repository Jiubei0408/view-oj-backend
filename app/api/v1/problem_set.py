from flask import jsonify
from flask_login import login_required

from app.libs.error_code import Success
from app.libs.red_print import RedPrint
from app.models.problem_set import create_problem_set, modify_problem_set, delete_problem_set, get_problem_set_list
from app.validators.forms import ProblemSetInfoForm, ModifyProblemSetForm, ProblemSetIdForm, PageForm

api = RedPrint('problem_set')


@api.route("/create_problem_set", methods=['POST'])
@login_required
def create_problem_set_api():
    form = ProblemSetInfoForm().validate_for_api()
    create_problem_set(form.problem_set_name.data, form.problem_id_list.data)
    return Success('Create problem set successful')


@api.route("/modify_problem_set", methods=['POST'])
@login_required
def modify_problem_set_api():
    form = ModifyProblemSetForm().validate_for_api()
    modify_problem_set(form.problem_set_id.data, form.problem_set_name.data, form.problem_id_list.data)
    return Success('Modify problem set successful')


@api.route("/delete_problem_set", methods=['POST'])
@login_required
def delete_problem_set_api():
    form = ProblemSetIdForm().validate_for_api()
    delete_problem_set(form.problem_set_id.data)
    return Success('Delete problem set successful')


@api.route("/get_problem_set_list", methods=['POST'])
@login_required
def get_problem_set_list_api():
    form = PageForm().validate_for_api()
    res = get_problem_set_list(form.page.data, form.page_size.data)
    return jsonify({
        'code': 0,
        'data': res
    })
