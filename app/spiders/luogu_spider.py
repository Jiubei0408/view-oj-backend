import json
import re
import execjs
from urllib.parse import unquote

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class LuoguHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'host': 'www.luogu.com.cn'
        }
        self.headers.update(headers)


class LuoguSpider(BaseSpider):
    @staticmethod
    def _get_user_id(username):
        url = 'https://www.luogu.com.cn/fe/api/user/search?keyword={}'.format(username)
        res = LuoguHttp().get(url=url)
        res_json = json.loads(res.text)
        return res_json['users'][0]['uid']

    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        url = 'https://www.luogu.com.cn/user/{}'.format(self._get_user_id(username))
        res = LuoguHttp().get(url=url)
        res_raw = re.search(r'decodeURIComponent\("(.*)"\)\);', res.text).group(1)
        res_str = unquote(res_raw)
        res_json = execjs.eval(res_str)

        accept_problem_list = []
        for problem in res_json['currentData']['passedProblems']:
            accept_problem_list.append(problem['pid'])

        return accept_problem_list

    def get_problem_info(self, problem_id):
        url = 'https://www.luogu.com.cn/problem/P{}'.format(problem_id)
        res = LuoguHttp().get(url=url)

        try:
            res_raw = re.search(r'decodeURIComponent\("(.*)"\)\);', res.text).group(1)
            res_str = unquote(res_raw)
            res_json = execjs.eval(res_str)

            total = res_json['currentData']['problem']['totalSubmit']
            accept = res_json['currentData']['problem']['totalAccepted']

            rating = int(calculate_problem_rating(total, accept) * 1.1)

        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = 'sumingzeng'
    print(LuoguSpider().get_user_info(oj_username))
    print(LuoguSpider().get_problem_info('1001'))
