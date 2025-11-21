#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
系统管理路由
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

bp = Blueprint('system', __name__)


@bp.route('/info', methods=['GET'])
@jwt_required()
def get_system_info():
    """获取系统信息"""
    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'version': '1.0.0',
            'name': '雅达管理（财税版）'
        }
    })
