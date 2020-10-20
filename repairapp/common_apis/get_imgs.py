# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/20
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
from flask import Blueprint, send_from_directory
from flask_restful import Resource, Api, reqparse

get_imgs_bp = Blueprint('get_imgs', __name__)
api = Api(get_imgs_bp)


class GetImgs(Resource):
    def get(self):
        ...

    def post(self):
        ...

    def put(self):
        ...

    def delete(self):
        ...

api.add_resource(GetImgs, '/repairapp/v1/get/imgs')