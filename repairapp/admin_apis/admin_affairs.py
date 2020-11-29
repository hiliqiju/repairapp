# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/19
"""
import flask_restful
from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from repairapp.customabort import custom_abort
from repairapp.models import Repair, Users

admin_affair_bp = Blueprint('admin_affair', __name__)
api = Api(admin_affair_bp)

affair_fields = {
    'id': fields.Integer,
    'img_name': fields.String,
    'desc': fields.String,
    'remark': fields.String,
    'site': fields.String,
    'repair_date': fields.DateTime,
    'status': fields.String
}

resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(affair_fields))
}


def get_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return parses.parse_args()


def get_del_parses():
    del_parses = reqparse.RequestParser()
    del_parses.add_argument('id', type=str, location='form', required=True, help='id是必须的')
    del_parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return del_parses.parse_args()


# 自定义msg
flask_restful.abort = custom_abort


class AdminAffair(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = get_parses()
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return user

        affairs = Repair.query.all()
        return {
            'code': 2000,
            'msg': '返回成功',
            'data': affairs
        }

    def post(self):
        ...

    def put(self):
        ...

    def delete(self):
        args = get_del_parses()
        id = args.get('id')
        # 获取并验证token
        token = args.get('token')
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        res = Repair.query.filter(Repair.id == id).delete()
        if not res:
            return jsonify({
                'code': 4000,
                'msg': '删除失败'
            })
        else:
            return {
                'code': 2000,
                'msg': '删除成功',
            }


api.add_resource(AdminAffair, '/repairapp/v1/del/affairs', endpoint='admin_affairs')
