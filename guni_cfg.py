# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/23
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
import os

# 用于处理工作的并发进程的数量，默认为1
workers = 5
# 允许挂起的连接数的最大值
backlog = 2048
# 指定进程的工作方式，默认为同步方式sync
# worker_class = "sync"
# 指定进程的工作方式为异步
worker_class = "gevent"
# 开启调试模式
# debug = True
# 设置进程名称
proc_name = 'gunicorn.proc'
# 设置pid文件的文件名，如果不设置将不会创建
# pidfile = '/tmp/gunicorn.pid'
# 设置日志文件名
# logfile = '/var/log/gunicorn/debug.log'
# 定义错误日志输出等级
# loglevel = 'debug'
# 监听内网端口
bind = '0.0.0.0:80'
# 设置守护进程【关闭连接时，程序仍在运行】
daemon = True
# 设置超时时间120s，默认为30s。按自己的需求进行设置
timeout = 30
# 设置访问日志和错误信息日志路径
accesslog = '/www/wwwlogs/guni_access.log'
errorlog = '/www/wwwlogs/guni_error.log'
