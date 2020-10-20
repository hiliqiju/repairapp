# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/19
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
import os
from flask import Blueprint, jsonify, send_from_directory, g
from werkzeug.datastructures import FileStorage
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from repairapp.models import Repair
from repairapp.extentions import db

add_affairs_bp = Blueprint('add_affairs', __name__)
api = Api(add_affairs_bp)

affair_fields = {
    'img': fields.String,
    'desc': fields.String,
    'remark': fields.String,
    'site': fields.String,
    'repair_date': fields.DateTime(dt_format='iso8601'),
    'status': fields.String
}
resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(affair_fields))
}


def get_post_parses():
    post_parses = reqparse.RequestParser()
    # post_parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    post_parses.add_argument('img', type=FileStorage, location='files', required=True, help='img是必须的')
    post_parses.add_argument('desc', type=str, location='form', required=True, help='desc是必须的')
    post_parses.add_argument('remark', type=str, location='form', required=True, help='remark是必须的')
    post_parses.add_argument('site', type=str, location='form', required=True, help='site是必须的')
    return post_parses.parse_args()


class AddAffairs(Resource):
    @marshal_with(resource_fields)
    def get(self):
        # 获取并验证token
        # token = args.get('token')
        # 在token中得到当前用户id




        try:
            affairs = Repair.query.filter(Repair.user_id == 1).all()
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
                'data': affairs
            }

    def post(self):
        args = get_post_parses()
        # 获取并验证token
        # token = args.get('token')
        # 获取token中的 user_id





        img = args.get('img')
        desc = args.get('desc')
        user_id = 1
        remark = args.get('remark')
        site = args.get('site')
        img_path = os.path.join(g.PATH, img.filename)  # 得到img本地路径

        img.save(img_path)  # 将img存储到本地
        repair = Repair(desc, site, user_id, img_path, remark)
        try:
            db.session.add(repair)
        except Exception as e:
            print(f'------------Error------------{e}')
            return jsonify({
                'code': 5001,
                'msg': '服务异常'
            })
        else:
            return jsonify({
                'code': 2000,
                'msg': '添加成功',
            })

    def put(self):
        ...

    def delete(self):
        ...


api.add_resource(AddAffairs, '/repairapp/v1/add/affairs', endpoint='add_affairs')
