import re
from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class NowcoderSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        index = 1
        data = []
        pre = []
        while 1:
            url = 'https://ac.nowcoder.com/acm/contest/profile/{}/practice-coding?&pageSize=200&search=&statusTypeFilter=5&languageCategoryFilter=-1&orderType=DESC&page={}'.format(
                username, index)
            res = SpiderHttp().get(url=url)
            r = re.findall(r'/acm/problem/(\d+)', res.text)
            if r == pre:
                break
            data.extend(r)
            pre = r
            index += 1

        return data

    def get_problem_info(self, problem_id):
        return {'rating': DEFAULT_PROBLEM_RATING}


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = '4292239'
    print(NowcoderSpider().get_user_info(oj_username))
