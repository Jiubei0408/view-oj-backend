from app.config.setting import DEFAULT_PROBLEM_RATING
from app.models.accept_problem import create_accept_problem, get_accept_problem_list_by_oj_id
from app.models.oj import get_oj_by_oj_id, get_oj_by_oj_name, get_oj_list
from app.models.oj_username import get_oj_username
from app.models.problem import get_problem_by_problem_info, get_problem_by_problem_id, modify_problem_rating
# 导入spider
from app.models.task import get_task, create_task
from app.spiders.codeforces_spider import CodeforcesSpider
from app.spiders.hdu_spider import HduSpider
from app.spiders.luogu_spider import LuoguSpider
from app.spiders.poj_spider import PojSpider
from app.spiders.vjudge_spider import VjudgeSpider
from app.spiders.zoj_spider import ZojSpider
from app.spiders.zucc_spider import ZuccSpider
from app.spiders.hysbz_spider import HysbzSpider


def crawl_accept_problem(username, oj_id):
    oj_name = get_oj_by_oj_id(oj_id).name
    oj_username = get_oj_username(username, oj_id)
    if not oj_username:
        return
    oj_spider = globals()[oj_name.title() + 'Spider']

    already_accept_problem = dict()
    for i in get_oj_list():
        already_accept_problem[i['id']] = set(get_accept_problem_list_by_oj_id(username, i['id']))

    all_accept_problem = oj_spider().get_user_info(oj_username)
    if not all_accept_problem:
        return

    for problem_id in all_accept_problem:
        real_oj_id = oj_id
        if oj_name == 'vjudge':
            real_oj_name, problem_id = problem_id.split('-')
            real_oj_name = real_oj_name.lower()
            if real_oj_name == 'gym':
                real_oj_name = 'codeforces'

            real_oj_id = get_oj_by_oj_name(real_oj_name).id
        elif oj_name == 'luogu':
            if problem_id[0] == 'P':
                real_oj_name = 'luogu'
                problem_id = problem_id[1:]
            elif problem_id[0] == 'C':
                real_oj_name = 'codeforces'
                problem_id = problem_id[2:]
            elif problem_id[0] == 'S':
                real_oj_name = 'spoj'
                problem_id = problem_id[2:]
            elif problem_id[0] == 'A':
                real_oj_name = 'atcoder'
                problem_id = problem_id[2:]
            elif problem_id[0] == 'U':
                real_oj_name = 'uva'
                problem_id = problem_id[3:]
            else:
                continue

            real_oj_id = get_oj_by_oj_name(real_oj_name).id
        elif oj_name == 'codeforces':
            problem_id = "".join(problem_id.split('-'))

        if problem_id not in already_accept_problem.get(real_oj_id, set()):
            problem = get_problem_by_problem_info(real_oj_id, problem_id)
            if problem.rating == 0:
                crawl_problem_rating(problem.id)
                problem = get_problem_by_problem_info(real_oj_id, problem_id)
            create_accept_problem(username, problem.id, 0)


def crawl_problem_rating(problem_id):
    problem = get_problem_by_problem_id(problem_id)
    if problem.oj.status == 0:
        modify_problem_rating(problem_id, DEFAULT_PROBLEM_RATING)
        return
    oj_name = problem.oj.name
    oj_spider = globals()[oj_name.title() + 'Spider']
    problem_pid = problem.problem_pid
    rating = oj_spider().get_problem_info(problem_pid)['rating']
    modify_problem_rating(problem_id, rating)


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = crawl_problem_rating(5320)
    print(r)
