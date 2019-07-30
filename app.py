import json
import time

from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError
from app.models.task import finish_task, get_an_idle_task, start_task
from app.spiders.oj_spider import crawl_accept_problem, crawl_problem_rating
from threading import Thread

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 调试模式
        # log
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


def task_executor():
    with create_app().app_context():
        while 1:
            try:
                task = get_an_idle_task()
                if task:
                    start_task(task.id)
                    try:
                        kwargs = json.loads(task.kwargs)
                        if task.task_name == 'crawl_accept_problem':
                            crawl_accept_problem(**kwargs)
                        elif task.task_name == 'crawl_problem_rating':
                            crawl_problem_rating(**kwargs)
                    except:
                        pass
                    finish_task(task.id)
                time.sleep(1)
            except:
                time.sleep(10)


if __name__ == '__main__':
    print('start task executor')
    Thread(target=task_executor, daemon=True).start()
    print('start web server')
    app.run(host="0.0.0.0", port=5000, debug=True)
