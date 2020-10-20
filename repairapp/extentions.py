# -*- coding: utf-8 -*-
"""
    @Author: liqiju
    @Email: helloliqiju@qq.com
    @Date: 2020/10/15
    @Gitee: https://gitee.com/missliqiju/repairapp.git
"""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
migrate = Migrate()
