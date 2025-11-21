#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask应用工厂
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config

# 初始化扩展
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

    # 注册蓝图
    from app.routes import auth, customer, business, finance, employee, statistics, system

    app.register_blueprint(auth.bp, url_prefix='/api/auth')
    app.register_blueprint(customer.bp, url_prefix='/api/customers')
    app.register_blueprint(business.bp, url_prefix='/api/business')
    app.register_blueprint(finance.bp, url_prefix='/api/finance')
    app.register_blueprint(employee.bp, url_prefix='/api/employees')
    app.register_blueprint(statistics.bp, url_prefix='/api/statistics')
    app.register_blueprint(system.bp, url_prefix='/api/system')

    # 注册错误处理
    register_error_handlers(app)

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app


def register_error_handlers(app):
    """注册错误处理器"""

    @app.errorhandler(400)
    def bad_request(error):
        return {'code': 400, 'message': '请求参数错误'}, 400

    @app.errorhandler(401)
    def unauthorized(error):
        return {'code': 401, 'message': '未授权访问'}, 401

    @app.errorhandler(403)
    def forbidden(error):
        return {'code': 403, 'message': '禁止访问'}, 403

    @app.errorhandler(404)
    def not_found(error):
        return {'code': 404, 'message': '资源不存在'}, 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return {'code': 500, 'message': '服务器内部错误'}, 500
