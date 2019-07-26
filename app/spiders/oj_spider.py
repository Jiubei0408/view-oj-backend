from app.models.accept_problem import get_accept_problem_list, add_accept_problem
from app.models.oj import get_oj_by_oj_id, get_oj_id_by_oj_name, get_all_oj
from app.models.oj_username import get_oj_username

from app.spiders.codeforces_spider import CodeforcesSpider
from app.spiders.hdu_spider import HduSpider
from app.spiders.luogu_spider import LuoguSpider
from app.spiders.poj_spider import PojSpider
from app.spiders.vjudge_spider import VjudgeSpider
from app.spiders.zoj_spider import ZojSpider
from app.spiders.zucc_spider import ZuccSpider


def crawl_oj_info(user_id, oj_id):
    oj_name = get_oj_by_oj_id(oj_id)
    oj_username = get_oj_username(user_id, oj_id)
    if not oj_username:
        return
    oj_spider = globals()[oj_name.title() + 'Spider']

    already_accept_problem = dict()
    for i in get_all_oj():
        already_accept_problem[i['id']] = set(get_accept_problem_list(user_id, i['id']))

    all_accept_problem = oj_spider.get_user_info(oj_username)
    if not all_accept_problem:
        return

    for problem_id in all_accept_problem:
        real_oj_id = oj_id
        if oj_name == 'vjudge':
            real_oj_name, problem_id = problem_id.split('-')
            real_oj_name = real_oj_name.lower()
            if real_oj_name == 'gym':
                real_oj_name = 'codeforces'

            real_oj_id = get_oj_id_by_oj_name(real_oj_name)
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

            real_oj_id = get_oj_id_by_oj_name(real_oj_name)
        elif oj_name == 'codeforces':
            problem_id = "".join(problem_id.split('-'))

        if problem_id not in already_accept_problem.get(real_oj_id, set()):
            add_accept_problem(user_id, real_oj_id, problem_id)

    # TODO 计算rating
    pass


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = crawl_oj_info(15, 5)
    print(r)
