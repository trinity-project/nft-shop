# -*- coding: utf-8 -*-
import os
import multiprocessing

d_venv = os.environ.get('APP_ENV')

if not d_venv or d_venv.lower() in ["dev", "test"]:
    #worker数量
    workers=2
    #绑定的端口
    bind='127.0.0.1:8088'
else:
    workers=2
    bind='127.0.0.1:8081'
# 监听队列
backlog=2048
#Workers silent for more than this many seconds are killed and restarted
timeout = 30
#Generally set in the 1-5 seconds #
keepalive=8
proc_name='gunicorn.pid'
if not d_venv:
    errorlog='/Users/xu/log/wob/error.log'
    accesslog='/Users/xu/log/wob/access.log'
elif d_venv.lower() in ["test", "prod"]:
    errorlog='/home/wob/log/error.txt'
    accesslog='/home/wob/log/access.txt'
# 错误日志级别，访问日志级别无法设置
loglevel='warning'