from app import create_app
from app.models.oj import get_all_oj
from app.models.user import get_all_user
from app.spiders.oj_spider import crawl_oj_info

with create_app().app_context():
    for user_id in get_all_user():
        for oj_id in get_all_oj():
            if oj_id['status']:
                crawl_oj_info(user_id, oj_id['id'])
