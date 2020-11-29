# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/18
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
import flask_restful
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from repairapp.customabort import custom_abort
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


def get_put_parses():
    post_parses = reqparse.RequestParser()
    post_parses.add_argument('file', type=str, location='form', required=True, help='文件是必需的')
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


# 自定义msg
flask_restful.abort = custom_abort


class AdminUsers(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = get_parses()
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return user

        users = Users.query.filter(Users.permission == '0').all()
        return {
            'code': 2000,
            'msg': '请求成功',
            'data': users
        }

    def post(self):
        args = get_post_parses()
        token = args.get('token')
        username = args.get('username')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        if Users.query.filter(Users.username == username).first():
            return jsonify({
                'code': 4000,
                'msg': '该用户已存在'
            })
        else:
            new_user = Users(username)
            new_user.set_password()
            db.session.add(new_user)
            return jsonify({
                'code': 2000,
                'msg': '添加成功'
            })

    def put(self):
        args = get_del_parses()
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        def user_init_func(row):
            c = Users(row['无', 'username', '无', '无', '无'], )
            return c

        request.save_book_to_database(
            field_name='file',
            session=db.session,
            tables=[Users],
            initializers=[user_init_func]
        )

    def delete(self):
        args = get_del_parses()
        token = args.get('token')
        id = args.get('id')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        res = Users.query.filter(Users.id == id).delete()
        if not res:
            return jsonify({
                'code': 4000,
                'msg': '删除失败'
            })
        else:
            return jsonify({
                'code': 2000,
                'msg': '删除成功'
            })


api.add_resource(AdminUsers, '/repairapp/v1/users', endpoint='admin_users')
