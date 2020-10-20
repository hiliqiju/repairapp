# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/19
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with

handle_affairs_bp = Blueprint('handle_affairs', __name__)
api = Api(handle_affairs_bp)


class HandleAffairs(Resource):
    def get(self):
        ...

    def post(self):
        ...

    def put(self):
        ...

    def delete(self):
        ...


api.add_resource(HandleAffairs, '/repairapp/v1/handle', endpoint='handle_affairs')
