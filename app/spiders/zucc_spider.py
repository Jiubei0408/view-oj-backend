import re

from app.config.setting import *
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class ZUCCSpider(BaseSpider):
    @staticmethod
    def get_user_info(username):
        url = 'http://acm.zucc.edu.cn/userinfo.php?user={}'.format(username)
        res = SpiderHttp().get(url=url)

        r = re.findall(r'p\((\d+),\d+\);', res.text)
        return r

    @staticmethod
    def get_problem_info(problem_id):
        url = 'http://acm.zucc.edu.cn/problem.php?id={}'.format(problem_id)
        res = SpiderHttp().get(url=url)

        try:
            total = int(re.search(r'Submit: </span>(\d+)(&nbsp;)*<span', res.text).group(1))
            accept = int(re.search(r'Solved: </span>(\d+)(&nbsp;)*<br>', res.text).group(1))
            rating = calculate_problem_rating(total, accept)
        except:
            rating = PROBLEM_DEFAULT_RATING

        return {'rating': rating}


if __name__ == '__main__':
    print(ZUCCSpider.get_problem_info('1000'))
