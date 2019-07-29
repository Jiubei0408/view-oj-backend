import json
import re

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class HduSpider(BaseSpider):
    @staticmethod
    def get_user_info(username):
        url = 'http://new.npuacm.info/api/crawlers/hdu/{}'.format(username)
        res = SpiderHttp().get(url=url)
        res_json = json.loads(res.text)
        return res_json.get('data', dict()).get('solvedList', list())

    @staticmethod
    def get_problem_info(problem_id):
        url = 'http://acm.hdu.edu.cn/showproblem.php?pid={}'.format(problem_id)
        res = SpiderHttp().get(url=url)
        try:
            re_res = re.search(r'<br>Total Submission\(s\): (\d+)(&nbsp;){4}Accepted Submission\(s\): (\d+)<br>',
                               res.text)
            total = int(re_res.group(1))
            accept = int(re_res.group(3))
            rating = calculate_problem_rating(total, accept)
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    print(HduSpider.get_problem_info('1000'))
