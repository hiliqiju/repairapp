# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/15
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
import os
from flask import Flask, jsonify, g
from repairapp.settings import config
from repairapp.models import Users
from repairapp.extentions import db, bcrypt, cors, migrate
from repairapp.common_apis.login import login_bp
from repairapp.common_apis.modify_pwd import mod_pwd_bp
from repairapp.admin_apis.admin_users import admin_users_bp
from repairapp.admin_apis.admin_techns import admin_techn_bp
from repairapp.admin_apis.admin_affairs import admin_affair_bp
from repairapp.users_apis.add_affairs import add_affairs_bp
from repairapp.techns_apis.handle_affairs import handle_affairs_bp


# 数据库迁移(需导入models.Users)
# flask db --help
def create_app(configName=None):
    if configName is None:
        configName = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    # 导入配置文件
    app.config.from_object(config[configName])
    # 注册全局变量
    register_before_request(app)
    # 注册扩展
    register_extentions(app)
    # 注册蓝图
    register_blueprints(app)
    # 注册错误
    register_errors(app)
    return app


def register_extentions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/repairapp/v1/*": {"origins": "*"}})


def register_blueprints(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(mod_pwd_bp)
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(admin_techn_bp)
    app.register_blueprint(admin_affair_bp)
    app.register_blueprint(add_affairs_bp)
    app.register_blueprint(handle_affairs_bp)


def register_before_request(app):
    @app.before_request
    def before_request():
        g.PATH = os.path.join(app.root_path, 'static/imgs')


def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({
            'code': 404,
            'msg': '接口调用错误'
        })

    @app.errorhandler(500)
    def interal_server_error(e):
        return jsonify({
            'code': 500,
            'msg': '服务器错误'
        })
