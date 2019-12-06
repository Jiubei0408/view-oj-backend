import json
import re
import execjs
from urllib.parse import unquote

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class JskSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        page = 1
        accept_list = []
        while True:
            url = 'https://i.jisuanke.com/timeline/nanti/{}?page={}'.format(username, page)
            res = SpiderHttp().get(url=url)
            res_json = json.loads(res.text)
            if not res_json['data']:
                break
            for data in res_json['data']:
                problem_url = data['url']
                problem_id = re.findall(r'//nanti.jisuanke.com/t/(.*)', problem_url)[0]
                # 需要kv表优化
                res = SpiderHttp().get(url='https:'+problem_url)
                actual_url = res.history[1].url
                problem_id = re.findall('http://nanti.jisuanke.com/t/(.*)', actual_url)[0]
                accept_list.append(problem_id)
            page += 1
        return accept_list

    def get_problem_info(self, problem_id):
        try:
            url = 'https://nanti.jisuanke.com/t/{}'.format(problem_id)
            res = SpiderHttp().get(url=url)
            data = re.findall(r'通过 (\d+) 人次 / 提交 (\d+) 人次', res.text)
            accept = int(data[0][0])
            total = int(data[0][1])
            rating = int(calculate_problem_rating(total, accept))

        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = '4lkvgc2'
    print(JskSpider().get_user_info(oj_username))
