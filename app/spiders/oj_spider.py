from app.models.accept_problem import get_accept_problem_list, add_accept_problem
from app.models.oj import get_oj_by_oj_id, get_oj_id_by_oj_name, get_all_oj
from app.models.oj_username import get_oj_username
from app.models.user import get_all_user
from app.spiders.codeforces_spider import CodeforcesSpider
from app.spiders.hdu_spider import HduSpider
from app.spiders.luogu_spider import LuoguSpider
from app.spiders.poj_spider import PojSpider
from app.spiders.vjudge_spider import VjudgeSpider
from app.spiders.zoj_spider import ZojSpider
from app.spiders.zucc_spider import ZuccSpider


def crawl_oj_info(user_id, oj_id):
    oj_name = get_oj_by_oj_id(oj_id).title()
    oj_username = get_oj_username(user_id, oj_id)
    if not oj_username:
        return
    oj_spider = globals()[oj_name + 'Spider']

    already_accept_problem = get_accept_problem_list(user_id, oj_id)
    all_accept_problem = oj_spider.get_user_info(oj_username)
    now_accept_problem = set(all_accept_problem) - set(already_accept_problem)

    for problem_id in now_accept_problem:

        if oj_name == 'Vjudge':
            real_oj_name, real_problem_id = problem_id.split('-')
            real_oj_name = real_oj_name.lower()
            real_oj_id = get_oj_id_by_oj_name(real_oj_name)
            add_accept_problem(user_id, real_oj_id, real_problem_id)
            pass
        else:
            add_accept_problem(user_id, oj_id, problem_id)

    # TODO 计算rating
    pass


def crawl_all_oj_info(user_id=None):
    if user_id:
        user_id_list = [user_id]
    else:
        user_id_list = get_all_user()

    for user_id in user_id_list:
        for oj_id in get_all_oj():
            if oj_id['status']:
                crawl_oj_info(user_id, oj_id['id'])


if __name__ == '__main__':
    from app import create_app

    with create_app().app_context():
        r = crawl_oj_info(3, 12)
    print(r)
