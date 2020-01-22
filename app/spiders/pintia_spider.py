import json
import time

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.spiders.cookies import Cookies
from app.spiders.jigsaw import Jigsaw
from app.spiders.spider_http import SpiderHttp
from app.models.oj_username import modify_oj_username


class PintiaHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': 'application/json;charset=UTF-8'
        }
        self.headers.update(headers)

    limit: int = 500
    lastreq: int = 0

    def time(self):
        return int(time.time() * 1000)

    def checklimit(self):
        return self.time() - self.lastreq >= self.limit

    def get(self, **kwargs):
        while not self.checklimit():
            time.sleep(self.limit / 1000)
        self.lastreq = self.time()
        return self._request('GET', **kwargs)

    def post(self, **kwargs):
        while not self.checklimit():
            time.sleep(self.limit / 1000)
        self.lastreq = self.time()
        return self._request('POST', **kwargs)


class PintiaSpider(BaseSpider):
    problem_set = [
        ('91827364500', 'Z'),  # ZOJ
        ('994805046380707840', 'L'),  # 天梯赛
        ('994805148990160896', 'T'),  # 顶级
        ('994805342720868352', 'A'),  # 甲级
        ('994805260223102976', 'B'),  # 乙级
    ]
    pintia_http = PintiaHttp()

    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        password = oj_username.oj_password
        try:
            cookies = json.loads(oj_username.oj_cookies)
            headers = {
                'Cookie': Cookies.dict_to_str(cookies)
            }
            self.pintia_http.headers.update(headers)
            assert self.check_cookies(username)
        except:
            cookies = self.get_cookies(username, password)
            modify_oj_username(oj_username.username, oj_username.oj_id, oj_username.oj_username,
                               oj_username.oj_password, json.dumps(cookies))
            assert self.check_cookies(username)

        accept_problem_list = []

        for problem_set_id, tag in self.problem_set:
            url = 'https://pintia.cn/api/problem-sets/{}/exam-problem-status'.format(problem_set_id)
            res = self.pintia_http.get(url=url).json()
            for problem in res.get('problemStatus', []):
                if problem['problemSubmissionStatus'] == 'PROBLEM_ACCEPTED':
                    accept_problem_list.append(tag + '-' + problem['label'])

        return accept_problem_list

    def get_problem_info(self, problem_id):
        return {'rating': DEFAULT_PROBLEM_RATING}

    def check_cookies(self, email):
        url = 'https://pintia.cn/api/u/current'
        res = self.pintia_http.get(url=url).json()
        if not res.get('user'):
            return False
        if res['user']['email'] != email:
            return False
        return True

    def get_cookies(self, email, password):
        jigsaw = Jigsaw('https://pintia.cn/auth/login?redirect=https%3A%2F%2Fpintia.cn%2F', headless=False)

        jigsaw.send_keys(email, '//input[@name="email"]')
        jigsaw.send_keys(password, '//input[@name="password"]')
        jigsaw.click('//button[@class="btn btn-primary"]')

        t = 0
        while 1:
            t += 1
            try:
                time.sleep(3)
                jigsaw.run()
                jigsaw.url_to_be('https://pintia.cn/problem-sets?tab=0')
                break
            except:
                if t >= 10:
                    raise Exception('login fail')
        cookies = jigsaw.get_cookies()
        jigsaw.close()
        cookies = Cookies.list_to_dict(cookies)
        headers = {
            'Cookie': Cookies.dict_to_str(cookies)
        }
        self.pintia_http.headers.update(headers)
        return cookies


if __name__ == '__main__':
    def f(username):
        from app import create_app
        from app.models.oj_username import get_oj_username

        create_app().app_context().push()
        temp = PintiaSpider().get_user_info(get_oj_username(username, 25))
        print(username, len(temp), temp)

    from threading import Thread

    for i in range(0, 10):
        t = Thread(target=f, args=['31801054'])
        t.start()
