# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/19
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
import os
from flask import Blueprint, jsonify, g
from werkzeug.datastructures import FileStorage
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from repairapp.models import Repair, Users
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
    post_parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    post_parses.add_argument('img', type=FileStorage, location='files')
    post_parses.add_argument('desc', type=str, location='form', required=True, help='desc是必须的')
    post_parses.add_argument('remark', type=str, location='form')
    post_parses.add_argument('site', type=str, location='form', required=True, help='site是必须的')
    return post_parses.parse_args()


def get_parses():
    get_parses = reqparse.RequestParser()
    get_parses.add_argument('token', type=str, location='headers', required=True, help='无token')
    return get_parses.parse_args()


class AddAffairs(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = get_parses()
        token = args.get('token')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return user
        # 在token中得到当前用户id
        id = user.id
        # 获取用户id的所有报修信息
        affairs = Repair.query.filter(Repair.user_id == id).all()
        return {
            'code': 2000,
            'msg': '请求成功',
            'data': affairs
        }

    def post(self):
        args = get_post_parses()
        token = args.get('token')
        img = args.get('img')
        desc = args.get('desc')
        remark = args.get('remark')
        site = args.get('site')
        # 获取并验证token
        user = Users.verify_token(token)
        if type(user) is dict:
            return jsonify(user)
        # 获取token中的 user_id
        id = user.id
        # 判断表单参数是否为null
        if img is not None:
            img_name = img.filename  # 得到img本地路径
            img.save(os.path.join(g.PATH, img.filename))  # 将img存储到本地
        else:
            img_name = '无'
        if remark == '':
            remark = '无'
        db.session.add(Repair(desc, site, id, img_name, remark))
        return jsonify({
            'code': 2000,
            'msg': '添加成功',
        })

    def put(self):
        ...

    def delete(self):
        ...


api.add_resource(AddAffairs, '/repairapp/v1/add/affairs', endpoint='add_affairs')
