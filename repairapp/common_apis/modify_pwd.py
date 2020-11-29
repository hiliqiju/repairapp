# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/17
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
import flask_restful
from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from repairapp.customabort import custom_abort
from repairapp.models import Users

mod_pwd_bp = Blueprint('mod_pwd', __name__)
api = Api(mod_pwd_bp)

parses = reqparse.RequestParser()


def new_pwd_parses():
    parses.add_argument('old_pwd', type=str, location='form', required=True, help='旧密码未填写')
    parses.add_argument('new_pwd', type=str, location='form', required=True, help='密码未填写')
    parses.add_argument('conf_pwd', type=str, location='form', required=True, help='确认密码未填写')
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return parses.parse_args()


# 自定义msg
flask_restful.abort = custom_abort


class ModifyPwd(Resource):
    def get(self):
        ...

    def post(self):
        ...

    def put(self):
        args = new_pwd_parses()
        token = args.get('token')
        old_pwd = args.get('old_pwd')
        new_pwd = args.get('new_pwd')
        conf_pwd = args.get('conf_pwd')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        # 验证旧密码
        if not Users(user.username, user.password).check_password(old_pwd):
            return jsonify({
                'code': 4000,
                'msg': '密码不正确'
            })
        elif new_pwd != conf_pwd:
            return jsonify({
                'code': 4000,
                'msg': '密码不一致！'
            })
        else:
            res = Users.query.filter(Users.id == user.id).update({
                'password': Users.set_new_password(new_pwd)
            })
            if not res:
                return jsonify({
                    'code': 4000,
                    'msg': '修改失败'
                })
            else:
                return jsonify({
                    'code': 2000,
                    'msg': '修改成功'
                })

    def delete(self):
        ...


api.add_resource(ModifyPwd, '/repairapp/v1/mod_pwd', endpoint='mod_pwd')
