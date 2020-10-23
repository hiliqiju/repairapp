# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/20
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
from flask import Blueprint, send_from_directory, g
from flask_restful import Resource, Api, reqparse

get_imgs_bp = Blueprint('get_imgs', __name__)
api = Api(get_imgs_bp)


def get_parses():
    parses = reqparse.RequestParser()
    parses.add_argument('img_name', type=str, location='args', )
    return parses.parse_args()


class GetImgs(Resource):
    # <img src="http://127.0.0.1:5000/repairapp/v1/get/imgs?img_name=lemon.jpg">
    def get(self):
        args = get_parses()
        img_name = args.get('img_name')
        return send_from_directory(g.PATH, img_name)

    def post(self):
        ...

    def put(self):
        ...

    def delete(self):
        ...


api.add_resource(GetImgs, '/repairapp/v1/get/imgs')
