# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/17
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from repairapp.models import Users

mod_pwd_bp = Blueprint('mod_pwd', __name__)
api = Api(mod_pwd_bp)

parses = reqparse.RequestParser()


def old_pwd_parses():
    parses.add_argument('old_pwd', type=str, location='form')
    parses.add_argument('token', type=str, location='headers', required=True, help='token是必须的')
    return parses.parse_args()


def new_pwd_parses():
    parses.add_argument('new_pwd', type=str, location='form')
    parses.add_argument('conf_pwd', type=str, location='form')
    parses.add_argument('token', type=str, location='headers', required=True, help='token是必须的')
    return parses.parse_args()


custom_fields = {
    'code': fields.Integer,
    'msg': fields.String
}


class ModifyPwd(Resource):
    def get(self):
        ...

    @marshal_with(custom_fields)
    def post(self):
        args = old_pwd_parses()
        old_pwd = args.get('old_pwd')
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)

        if type(user) is dict:
            return jsonify(user)
        # 验证密码
        if not Users(user.username, user.password).check_password(old_pwd):
            return {
                'code': 2002,
                'msg': '密码不正确'
            }
        else:
            return {
                'code': 2000,
                'msg': '密码正确'
            }

    @marshal_with(custom_fields)
    def put(self):
        args = new_pwd_parses()
        token = args.get('token')
        new_pwd = args.get('new_pwd')
        conf_pwd = args.get('conf_pwd')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)
        # 假设前端验证密码已成功
        try:
            Users.query.filter(Users.id == user.id).update({
                'password': Users.set_new_password(new_pwd)
            })
        except Exception as e:
            print(f'---------------------{e}')
            return {
                'code': 2004,
                'msg': '密码错误'
            }
        else:
            return {
                'code': 2000,
                'msg': '修改成功'
            }

    def delete(self):
        ...


api.add_resource(ModifyPwd, '/repairapp/v1/mod_pwd', endpoint='mod_pwd')
