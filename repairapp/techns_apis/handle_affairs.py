# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/19
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from repairapp.models import Users, Repair

handle_affairs_bp = Blueprint('handle_affairs', __name__)
api = Api(handle_affairs_bp)

affair_fields = {
    'id': fields.Integer,
    'img': fields.String,
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


def get_put_parses():
    put_parses = reqparse.RequestParser()
    put_parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    put_parses.add_argument('id', type=int, location='form', required=True, help='id字段是必须的')
    put_parses.add_argument('status', type=str, location='form', required=True, help='status字段是必须的')
    return put_parses.parse_args()


class HandleAffairs(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = get_parses()
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        try:
            affairs = Repair.query.filter(Repair.status == '待处理').all()
        except Exception as e:
            print(f'-----------Error-----------{e}')
            return jsonify({
                'code': 5001,
                'msg': '服务异常'
            })
        else:
            return {
                'code': 2000,
                'msg': '返回成功',
                'data': affairs
            }

    def post(self):
        ...

    def put(self):
        args = get_put_parses()
        status = args.get('status')
        id = args.get('id')
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)

        try:
            Repair.query.filter(Repair.id == id).update({
                'status': status
            })
        except Exception as e:
            print(f'---------------------{e}')
            return {
                'code': 2004,
                'msg': '修改错误'
            }
        else:
            return {
                'code': 2000,
                'msg': '修改成功'
            }

    def delete(self):
        ...


api.add_resource(HandleAffairs, '/repairapp/v1/handle', endpoint='handle_affairs')
