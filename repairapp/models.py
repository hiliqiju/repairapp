# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/15
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
from repairapp.extentions import db, bcrypt
from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    regist_date = db.Column(db.DateTime, default=datetime.now)
    permission = db.Column(db.Enum('0', '1', '2'), default='0')
    repairs = db.relationship(
        'Repair',
        backref='users',
        lazy='dynamic'
    )

    def __init__(self, username, password='123456', permission='0'):
        self.username = username
        self.password = password
        self.permission = permission

    def set_password(self, password='123456'):
        self.password = bcrypt.generate_password_hash(password)

    def set_new_password(self, password='123456'):
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def generate_token(self, expiration=600):
        # 过期时间 600s
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            msg = {
                'code': 1002,
                'msg': 'token过期',
            }
        except BadSignature:
            msg = {
                'code': 1003,
                'msg': '无效的token',
            }
        else:
            msg = Users.query.get(data['id'])
        return msg


class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img_name = db.Column(db.String(100), nullable=True)
    desc = db.Column(db.String(500), nullable=False)  # 报修描述not null
    remark = db.Column(db.String(500), nullable=True)
    site = db.Column(db.String(50), nullable=False)  # 位置not null
    repair_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Enum('已处理', '待处理'), nullable=False)  # 状态not null
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # not null

    def __init__(self, desc, site, user_id, img_name, remark, status='待处理'):
        self.desc = desc
        self.site = site
        self.user_id = user_id
        self.img_name = img_name
        self.remark = remark
        self.status = status
