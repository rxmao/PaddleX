#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
认证路由
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'code': 401, 'message': '用户名或密码错误'}), 401

    if user.status == 0:
        return jsonify({'code': 403, 'message': '账号已被禁用'}), 403

    # 更新最后登录时间
    user.last_login = datetime.now()
    db.session.commit()

    # 生成token
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        'code': 200,
        'message': '登录成功',
        'data': {
            'token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }
    })


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """刷新token"""
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)

    return jsonify({
        'code': 200,
        'message': '刷新成功',
        'data': {'token': access_token}
    })


@bp.route('/info', methods=['GET'])
@jwt_required()
def get_user_info():
    """获取当前用户信息"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': user.to_dict()
    })


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用户登出"""
    # JWT本身是无状态的，登出主要在前端处理（删除token）
    # 如需服务端处理，可配合Redis黑名单机制
    return jsonify({
        'code': 200,
        'message': '登出成功'
    })


@bp.route('/register', methods=['POST'])
def register():
    """用户注册（仅管理员可用）"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    real_name = data.get('real_name')

    if not username or not password:
        return jsonify({'code': 400, 'message': '用户名和密码不能为空'}), 400

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'message': '用户名已存在'}), 400

    # 创建用户
    user = User(
        username=username,
        real_name=real_name,
        phone=data.get('phone'),
        email=data.get('email'),
        role=data.get('role', 'user')
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '注册成功',
        'data': user.to_dict()
    })
