import json
import re

from app.config.setting import *
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class LuoGuSpider(BaseSpider):
    @staticmethod
    def get_user_info(username):
        url = 'http://new.npuacm.info/api/crawlers/luogu/{}'.format(username)
        res = SpiderHttp().get(url=url)
        res_json = json.loads(res.text)
        return res_json

    @staticmethod
    def get_problem_info(problem_id):
        url = 'https://www.luogu.org/problemnew/show/{}'.format(problem_id)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'host': 'www.luogu.org'
        }
        res = SpiderHttp().get(url=url, headers=headers)

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
    print(LuoGuSpider.get_problem_info('P5413'))
