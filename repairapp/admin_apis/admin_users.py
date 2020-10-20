# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/18
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
from flask import Blueprint, jsonify
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from repairapp.models import Users
from repairapp.extentions import db

admin_users_bp = Blueprint('admin_users', __name__)
api = Api(admin_users_bp)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
}

resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(user_fields))
}


def get_post_parses():
    post_parses = reqparse.RequestParser()
    post_parses.add_argument('username', type=str, location='form', required=True, help='用户名是必需的')
    post_parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return post_parses.parse_args()


def get_del_parses():
    del_parses = reqparse.RequestParser()
    del_parses.add_argument('id', type=int, location='form', required=True, help='id是必需的')
    del_parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return del_parses.parse_args()


def get_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return parses.parse_args()


class AdminUsers(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = get_parses()
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        try:
            users = Users.query.filter(Users.permission == '0').all()
        except Exception as e:
            print(f'------------Error------------{e}')
            return jsonify({
                'code': 5001,
                'msg': '服务异常'
            })
        else:
            return {
                'code': 2000,
                'msg': '返回成功',
                'data': users
            }

    def post(self):
        args = get_post_parses()
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        username = args.get('username')
        new_user = Users(username)
        new_user.set_password()
        try:
            db.session.add(new_user)
        except Exception as e:
            print(f'-----------{e}')
            return jsonify({
                'code': 5001,
                'msg': '服务异常'
            })
        else:
            return jsonify({
                'code': 2000,
                'msg': '添加成功'
            })

    def put(self):
        ...

    def delete(self):
        args = get_del_parses()
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        id = args.get('id')
        try:
            db.session.delete(Users.query.filter(Users.id == id).first())
        except Exception as e:
            print(f'------------------{e}')
            return jsonify({
                'code': 5001,
                'msg': '服务异常'
            })
        else:
            return jsonify({
                'code': 2000,
                'msg': '删除成功'
            })


api.add_resource(AdminUsers, '/repairapp/v1/users', endpoint='admin_users')
