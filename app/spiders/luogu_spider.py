import json
import re
import execjs
from urllib.parse import unquote

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class LuoguHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'host': 'www.luogu.org'
        }
        self.headers.update(headers)


class LuoguSpider(BaseSpider):
    @staticmethod
    def get_user_id(username):
        url = 'https://www.luogu.org/space/ajax_getuid?username={}'.format(username)
        res = LuoguHttp().get(url=url)
        res_json = json.loads(res.text)
        return res_json.get('more', dict()).get('uid')

    def get_user_info(self, username, password):
        url = 'https://www.luogu.org/space/show?uid={}'.format(self.get_user_id(username))
        res = LuoguHttp().get(url=url)
        r = re.findall(
            '(?!<span style="display:none">\n)\[<a data-pjax href="/problemnew/show/.*">(.*)</a>\](?!\n</span>)',
            res.text)
        return r

    def get_problem_info(self, problem_id):
        url = 'https://www.luogu.org/problem/P{}'.format(problem_id)
        res = LuoguHttp().get(url=url)

        try:
            res_raw = re.search('decodeURIComponent\("(.*)"\)\);', res.text).group(1)
            res_str = unquote(res_raw)
            res_json = execjs.eval(res_str)

            difficulty = res_json['currentData']['problem']['difficulty']

            if difficulty == 1:
                rating = 800
            elif difficulty == 2:
                rating = 1200
            elif difficulty == 3:
                rating = 1600
            elif difficulty == 4:
                rating = 2000
            elif difficulty == 5:
                rating = 2400
            elif difficulty == 6:
                rating = 2800
            elif difficulty == 7:
                rating = 3200
            else:
                rating = DEFAULT_PROBLEM_RATING

        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    print(LuoguSpider().get_problem_info('1002'))
