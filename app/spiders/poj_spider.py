import json
import re

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class PojSpider(BaseSpider):
    @staticmethod
    def get_user_info(username):
        url = 'http://new.npuacm.info/api/crawlers/poj/{}'.format(username)
        res = SpiderHttp().get(url=url)
        res_json = json.loads(res.text)
        return res_json.get('data', dict()).get('solvedList', list())

    @staticmethod
    def get_problem_info(problem_id):
        url = 'http://poj.org/problem?id={}'.format(problem_id)
        res = SpiderHttp().get(url=url)
        try:
            total = int(re.search(r'<td><b>Total Submissions:</b> (\d+)</td>', res.text).group(1))
            accept = int(re.search(r'<td><b>Accepted:</b> (\d+)</td>', res.text).group(1))
            rating = calculate_problem_rating(total, accept)
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    print(PojSpider.get_problem_info('1000'))
