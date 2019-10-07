import json
from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class LojSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        url = 'http://new.npuacm.info/api/crawlers/loj/{}'.format(username)
        res = SpiderHttp().get(url=url)
        res_json = json.loads(res.text)
        return res_json.get('data', dict()).get('solvedList', list())

    def get_problem_info(self, problem_id):
        return {'rating': DEFAULT_PROBLEM_RATING}
