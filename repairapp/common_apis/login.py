# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/15
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from repairapp.models import Users

login_bp = Blueprint('login', __name__)
api = Api(login_bp)

user_fields = {
    'id': fields.String,
    'username': fields.String,
    'permission': fields.String,
    'regist_date': fields.DateTime
}
resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'token': fields.String,
    'data': fields.Nested(user_fields)
}


# 返回参数
def get_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('username', type=str, location=['form'], required=True, help='用户名是必填的')
    parses.add_argument('password', type=str, location=['form'], required=True, help='密码是必填的')
    return parses.parse_args()


class Login(Resource):
    def get(self):
        ...

    @marshal_with(resource_fields)
    def post(self):
        args = get_parses()
        username = args.get('username')
        password = args.get('password')
        user_result = Users.query.filter(
            Users.username == username).first()

        if not user_result:
            return {
                'msg': '用户不存在',
                'code': 4000,
            }
        elif not Users(username, user_result.password).check_password(password):
            return {
                'code': 4000,
                'msg': '密码不正确',
            }
        else:
            token = Users.generate_token(user_result)  # 生成token
            if user_result.permission == '0':
                return {
                    'code': 2000,
                    'msg': '普通用户登录成功',
                    'token': token,
                    'data': user_result
                }
            elif user_result.permission == '1':
                return {
                    'code': 2000,
                    'msg': '技工登录成功',
                    'token': token,
                    'data': user_result
                }
            else:
                return {
                    'code': 2000,
                    'msg': '管理员登录成功',
                    'token': token,
                    'data': user_result
                }

    def put(self):
        ...

    def delete(self):
        ...


api.add_resource(Login, '/repairapp/v1/login', endpoint='login')
