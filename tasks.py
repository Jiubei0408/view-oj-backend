from app import create_app
from app.models.oj import get_all_oj
from app.models.task import task_is_exist
from app.models.user import get_all_user
from app.spiders.oj_spider import task_crawl_oj_info

with create_app().app_context():
    for user in get_all_user():
        for oj in get_all_oj():
            if oj['status'] and user['status']:
                if not task_is_exist(user['id'], oj['id']):
                    task_crawl_oj_info(user['id'], oj['id'])
