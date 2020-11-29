# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/15
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
import os


class baseConfig:
    # SECRET_KEY = os.urandom(24)
    SECRET_KEY = 'EWIOH#&#@(&Fejfwo3&$J#&JFL#42KF34*(&H6FJWE'
    # flask_SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # 开启自动提交
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@127.0.0.1:3306/repairapp_db'


class development(baseConfig):
    ...


class production(baseConfig):
    ...


class testing(baseConfig):
    ...


config = {
    'development': development,
    'production': production,
    'testing': testing
}
