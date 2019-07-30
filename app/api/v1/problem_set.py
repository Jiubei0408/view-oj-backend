from flask import jsonify
from flask_login import login_required
from app.libs.red_print import RedPrint

api = RedPrint('problem_set')


@api.route("/create_problem_set", methods=['POST'])
@login_required
def create_problem_set_api():
    pass


@api.route("/modify_problem_set", methods=['POST'])
@login_required
def modify_problem_set_api():
    pass


@api.route("/delete_problem_set", methods=['POST'])
@login_required
def delete_problem_set_api():
    pass
