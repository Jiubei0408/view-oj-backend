import json
import time

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.spiders.cookies import Cookies
from app.spiders.jigsaw import Jigsaw
from app.spiders.spider_http import SpiderHttp


class PintiaHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': 'application/json;charset=UTF-8'
        }
        self.headers.update(headers)


class PintiaSpider(BaseSpider):
    problem_set = {
        '91827364500',  # ZOJ
        '994805046380707840',  # 天梯赛
        '994805148990160896',  # 顶级
        '994805342720868352',  # 甲级
        '994805260223102976',  # 乙级
    }
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

        for problem_set_id in self.problem_set:
            time.sleep(3)
            url = 'https://pintia.cn/api/problem-sets/{}/exam-problem-status'.format(problem_set_id)
            res = self.pintia_http.get(url=url).json()
            for problem in res.get('problemStatus', []):
                if problem['problemSubmissionStatus'] == 'PROBLEM_ACCEPTED':
                    accept_problem_list.append(problem['id'])
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
        jigsaw = Jigsaw('https://pintia.cn/auth/login?redirect=https%3A%2F%2Fpintia.cn%2F', headless=True)

        jigsaw.send_keys(email, '//*[@id="sparkling-daydream"]/div[3]/div/div[2]/form/div[1]/div/input')
        jigsaw.send_keys(password, '//*[@id="sparkling-daydream"]/div[3]/div/div[2]/form/div[2]/div/input')
        jigsaw.click('//*[@id="sparkling-daydream"]/div[3]/div/div[2]/form/div[4]/div/label/input')

        t = 0
        while 1:
            jigsaw.run()
            try:
                jigsaw.click('//*[@id="sparkling-daydream"]/div[3]/div/div[2]/form/div[6]/button')
                jigsaw.url_to_be('https://pintia.cn/problem-sets?tab=0')
                break
            except:
                t += 1
                if t >= 5:
                    raise Exception('验证失败')
        cookies = jigsaw.get_cookies()
        cookies = Cookies.list_to_dict(cookies)
        headers = {
            'Cookie': Cookies.dict_to_str(cookies)
        }
        self.pintia_http.headers.update(headers)
        return cookies


if __name__ == '__main__':
    from app import create_app
    from app.models.oj_username import get_oj_username, modify_oj_username

    create_app().app_context().push()

    print(PintiaSpider().get_user_info(get_oj_username('31702411', 25)))
