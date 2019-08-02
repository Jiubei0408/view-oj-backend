# oj_spider

接口文档: https://www.showdoc.cc/417895562132382

# 安装&&运行
```bash
# clone项目
git clone https://github.com/taoting1234/oj_spider

# 安装依赖
pip install requirements.txt

# 运行web服务器（测试环境）
python app.py

# 运行计划任务worker
celery -A tasks worker -l info -c 8 --pool=eventlet

# 运行计划任务beat
celery -A tasks beat -l info
```