import json
import re

from app.config.setting import *
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class CodeForcesSpider(BaseSpider):
    @staticmethod
    def get_user_info(username):
        url = 'http://new.npuacm.info/api/crawlers/codeforces/{}'.format(username)
        res = SpiderHttp().get(url=url)
        res_json = json.loads(res.text)
        return res_json.get('data', dict()).get('solvedList', list())

    @staticmethod
    def get_problem_info(problem_id):
        problem_id_1, problem_id_2 = problem_id.split('-')
        if int(problem_id_1) < 100000:  # 题目
            url = 'https://codeforces.com/problemset/problem/{}/{}'.format(problem_id_1, problem_id_2)
            res = SpiderHttp().get(url=url)
            try:
                rating = int(re.search(r'title="Difficulty">\s*\*(\d+)\s*</span>', res.text).group(1))
            except:
                rating = PROBLEM_DEFAULT_RATING
        else:  # gym
            rating = PROBLEM_DEFAULT_RATING

        return {'rating': rating}


if __name__ == '__main__':
    print(CodeForcesSpider.get_user_info('taoting'))
