# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/11/29
"""
from flask import jsonify
from flask_restful import abort


# 自定义msg
def custom_abort(http_status_code, *args, **kwargs):
    if http_status_code == 400:
        abort(jsonify({
            'code': 4000,
            'msg': '缺少必填项'
        }))
    return abort(http_status_code)
