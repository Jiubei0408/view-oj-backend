import json

from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class VJudgeSpider(BaseSpider):
    @staticmethod
    def get_user_info(username):
        url = 'http://new.npuacm.info/api/crawlers/vjudge/{}'.format(username)
        res = SpiderHttp().get(url=url)
        res_json = json.loads(res.text)
        return res_json

    @staticmethod
    def get_problem_info(problem_id):
        pass
