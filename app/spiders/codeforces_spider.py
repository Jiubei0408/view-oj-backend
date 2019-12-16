import json
import re

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp
import app.models.mapping as mapping
from bs4 import BeautifulSoup


class CodeforcesSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        page = 1
        accept_problem_list = []
        while True:
            url = 'http://codeforces.com/submissions/{}/page/{}'.format(username, page)
            res = SpiderHttp().get(url=url)
            soup = BeautifulSoup(res.text, 'lxml')
            res = soup.findAll('tr', {'data-submission-id': re.compile(r'[0-9]+?')})
            ok = False
            for i in res:
                if len(i.findAll('span', {'class': 'verdict-accepted'})) > 0:
                    problem = re.findall(r'/(\d+)/problem/([A-Za-z])',
                                         i.find('a', {'href': re.compile(r'.*/problem/.*')})['href'])
                    problem_id = '-'.join(problem[0])
                    if problem_id not in accept_problem_list:
                        accept_problem_list.append(problem_id)
                        ok = True
            if not ok:
                break
            page += 1
        return accept_problem_list

    def get_problem_info(self, problem_id):
        p = re.match('^([0-9]+)([a-zA-Z]+[0-9]*)$', problem_id)
        problem_id_1 = p.group(1)
        problem_id_2 = p.group(2)
        if int(problem_id_1) < 100000:  # 题目
            url = 'https://codeforces.com/problemset/problem/{}/{}'.format(problem_id_1, problem_id_2)
            res = SpiderHttp().get(url=url)
            try:
                rating = int(re.search(r'title="Difficulty">\s*\*(\d+)\s*</span>', res.text).group(1))
            except:
                rating = DEFAULT_PROBLEM_RATING
        else:  # gym
            try:
                rating = self._get_gym_constest_rating(problem_id_1)
            except:
                rating = DEFAULT_PROBLEM_RATING
        return {'rating': rating}

    @staticmethod
    def _get_gym_constest_rating(contest_id):
        star_rating = [DEFAULT_PROBLEM_RATING, 1200, 1600, 2000, 2400, 2800]
        stars = mapping.get_value('gym-{}'.format(contest_id))
        if stars is not None:
            return star_rating[int(stars)]
        url = 'https://codeforces.com/gyms'
        req = SpiderHttp()
        res = req.get(url=url)
        soup = BeautifulSoup(res.text, 'lxml')
        token = soup.find('input', {'name': 'csrf_token'})['value']
        res = req.post(url=url, data={
            'csrf_token': token,
            'searchByNameOrIdQuery': contest_id,
            'searchByProblem': False,
        })
        soup = BeautifulSoup(res.text, 'lxml')
        stars = len(soup.find('tr', {'data-contestid': contest_id}).findAll('img'))
        mapping.set_value('gym-{}'.format(contest_id), str(stars))
        return star_rating[stars]


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = 'boboge'
    print(CodeforcesSpider().get_user_info(oj_username))
