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
        star_rating = [0, 800, 1200, 1600, 2000, 2400]
        try:
            url = 'https://ac.nowcoder.com/acm/problem/list?keyword={}'.format(problem_id)
            res = SpiderHttp().get(url=url)
            data = re.findall(r'<td>\n(\d+)星\n</td>', res.text)
            star = int(data[0][0])
            rating = star_rating[star]
        except:
            rating = DEFAULT_PROBLEM_RATING
        return {'rating': rating}


if __name__ == '__main__':
    print(NowcoderSpider().get_problem_info('20123'))
