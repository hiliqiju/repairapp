# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/22
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
import click
from repairapp.models import Users, Repair
from repairapp.extentions import db


def register_commands(app):
    @app.cli.command('init_data')
    def init_data():
        """初始化表数据"""
        click.echo('initializing the table data...')
        # 初始化用户表数据
        user1 = Users('10001')
        user2 = Users('10002')
        user3 = Users('10003')
        user4 = Users('10004')
        user5 = Users('10005')
        for user in [user1, user2, user3, user4, user5]:
            user.set_password()
            db.session.add(user)
        techn1 = Users('20001', permission='1')
        techn2 = Users('20002', permission='1')
        techn3 = Users('20003', permission='1')
        for techns in [techn1, techn2, techn3]:
            techns.set_password()
            db.session.add(techns)
        admin = Users('11111', permission='2')
        admin.set_password()
        db.session.add(admin)
        # 初始化工单表数据
        affair1 = Repair('水龙头坏了，止不住', '东10-404', '1', '1603421966417.jpg', '十万火急')
        affair2 = Repair('地板烂了个大窟窿，走路不方便', '东1-501', '1', '1603421966396.jpg', '无', '待处理')
        affair3 = Repair('阳台围栏的玻璃碎了，恐高，有点害怕', '西11-707', '1', '1603421966400.jpg', '希望快一点来修')
        affair4 = Repair('浴室的下水管道堵住了', '东10-404', '2', '1603421966404.jpg', '快一点吧，水太多了')
        affair5 = Repair('厕所被舍友的充电宝堵住了，打捞不上来了', '东4-306', '2', '1603421966407.jpg', '太臭了，你再来晚一点就准备给我们收尸吧')
        affair6 = Repair('厕所的灯坏了', '东5-602', '3', '1603421966421.jpg', '不着急，慢慢来')
        affair7 = Repair('阳台玻璃门坏了，锁不住', '西10-104', '4', '1603421966411.jpg', '快一点来修，害怕有坏人')
        affair8 = Repair('柠檬坏了', '东3-306', '5', '无', '能不能帮我扔了')
        affair9 = Repair('风扇坏了，空调没坏', '西8-404', '2', '无', '无')
        affair10 = Repair('宿舍有蟑螂，太可怕了', '西18-204', '1', '无', '无')
        for affair in [affair1, affair2, affair3, affair4, affair5, affair6, affair7,
                       affair7, affair8, affair9, affair10]:
            db.session.add(affair)
        click.echo('initializing data success')
