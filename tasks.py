import os
import platform

from celery import Celery

from app import create_app
from app.models.oj import get_oj_list
from app.models.task import get_task, create_task, start_task, finish_task
from app.models.user import get_user_list
from app.spiders.oj_spider import crawl_accept_problem, crawl_problem_rating

# if platform.system() == 'Windows':
#     # 解决windows运行worker错误
#
#     os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

celery = Celery('tasks')
celery.config_from_object('app.config.setting')
celery.config_from_object('app.config.secure')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(3600, task_crawl_all_accept_problem, name='crawl_all_accept_problem')


@celery.task
def task_crawl_all_accept_problem():
    with create_app().app_context():
        for user in get_user_list():
            for oj in get_oj_list():
                if oj['status'] and user['status']:
                    task = get_task('crawl_accept_problem', {
                        'username': user['username'],
                        'oj_id': oj['id']
                    })
                    if not task or task.status == 2:
                        create_task('crawl_accept_problem', {
                            'username': user['username'],
                            'oj_id': oj['id']
                        })
                        task_crawl_accept_problem.delay(user['username'], oj['id'])


@celery.task
def task_crawl_accept_problem(username, oj_id):
    with create_app().app_context():
        start_task('crawl_accept_problem', {
            'username': username,
            'oj_id': oj_id
        })
        try:
            crawl_accept_problem(username, oj_id)
        except:
            pass
        finish_task('crawl_accept_problem', {
            'username': username,
            'oj_id': oj_id
        })


@celery.task
def task_crawl_problem_rating(problem_id):
    with create_app().app_context():
        start_task('crawl_problem_rating', {
            'problem_id': problem_id,
        })
        try:
            crawl_problem_rating(problem_id)
        except:
            pass
        finish_task('crawl_problem_rating', {
            'problem_id': problem_id,
        })
