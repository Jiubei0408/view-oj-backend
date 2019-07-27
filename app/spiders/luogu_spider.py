import json
import re

from app.config.setting import PROBLEM_DEFAULT_RATING
from app.libs.service import calculate_problem_rating
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

    @classmethod
    def get_user_info(cls, username):
        url = 'https://www.luogu.org/space/show?uid={}'.format(cls.get_user_id(username))
        res = LuoguHttp().get(url=url)
        r = re.findall(
            '(?!<span style="display:none">\n)\[<a data-pjax href="/problemnew/show/.*">(.*)</a>\](?!\n</span>)',
            res.text)
        return r

    @staticmethod
    def get_problem_info(problem_id):
        # TODO 已挂
        url = 'https://www.luogu.org/problemnew/show/{}'.format(problem_id)
        res = LuoguHttp().get(url=url)

        try:
            total_res = re.search(
                r'<span class="lg-bignum-num">([\d.]+)(<small>K</small>)*<small></small></span><span class="lg-bignum-text">提交</span>',
                res.text)
            total = float(total_res.group(1))
            if total_res.group(2):
                total *= 1000
            total = int(total)

            accept_res = re.search(
                r'<span class="lg-bignum-num">([\d.]+)(<small>K</small>)*<small></small></span><span class="lg-bignum-text">通过</span>',
                res.text)
            accept = float(accept_res.group(1))
            if accept_res.group(2):
                accept *= 1000
            accept = int(accept)

            rating = calculate_problem_rating(total, accept)
        except:
            rating = PROBLEM_DEFAULT_RATING

        return {'rating': rating}


if __name__ == '__main__':
    print(LuoguSpider.get_user_info('taoting'))
