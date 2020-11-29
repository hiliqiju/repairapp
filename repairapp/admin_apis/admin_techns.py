# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/18
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
import flask_restful
from flask import Blueprint, jsonify
from flask_restful import Resource, Api, fields, reqparse, marshal_with
from repairapp.customabort import custom_abort
from repairapp.models import Users
from repairapp.extentions import db

admin_techn_bp = Blueprint('admin_techn', __name__)
api = Api(admin_techn_bp)

techn_fields = {
    'id': fields.Integer,
    'username': fields.String,
}
resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(techn_fields))
}


def get_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return parses.parse_args()


def get_post_parses():
    post_parses = reqparse.RequestParser()
    post_parses.add_argument('username', type=str, location='form', required=True, help='用户名是必须的')
    post_parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return post_parses.parse_args()


def get_del_parses():
    del_parses = reqparse.RequestParser()
    del_parses.add_argument('id', type=int, location='form', required=True, help='id是必须的')
    del_parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return del_parses.parse_args()


# 自定义msg
flask_restful.abort = custom_abort


class AdminTechn(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = get_parses()
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return user

        techns = Users.query.filter(Users.permission == '1').all()
        return {
            'code': 2000,
            'msg': '请求成功',
            'data': techns
        }

    def post(self):
        args = get_post_parses()
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        username = args.get('username')
        if Users.query.filter(Users.username == username).first():
            return jsonify({
                'code': 4000,
                'msg': '该技工已存在'
            })
        else:
            techn = Users(username, '', '1')
            techn.set_password()
            db.session.add(techn)
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
        db.session.delete(Users.query.filter(Users.id == id).first())
        return jsonify({
            'code': 2000,
            'msg': '删除成功'
        })


api.add_resource(AdminTechn, '/repairapp/v1/techns', endpoint='admin_techn')
