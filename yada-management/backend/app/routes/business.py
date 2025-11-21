#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
业务路由
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.business import Business

bp = Blueprint('business', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_businesses():
    """获取业务列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    business_type = request.args.get('business_type', '')
    progress = request.args.get('progress', '')
    customer_id = request.args.get('customer_id', '', type=str)

    query = Business.query

    if business_type:
        query = query.filter_by(business_type=business_type)

    if progress:
        query = query.filter_by(progress=progress)

    if customer_id:
        query = query.filter_by(customer_id=int(customer_id))

    pagination = query.order_by(Business.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'items': [business.to_dict() for business in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@bp.route('/<int:business_id>', methods=['GET'])
@jwt_required()
def get_business(business_id):
    """获取业务详情"""
    business = Business.query.get(business_id)

    if not business:
        return jsonify({'code': 404, 'message': '业务不存在'}), 404

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': business.to_dict()
    })


@bp.route('', methods=['POST'])
@jwt_required()
def create_business():
    """创建业务"""
    user_id = get_jwt_identity()
    data = request.get_json()

    business = Business(
        customer_id=data.get('customer_id'),
        business_type=data.get('business_type'),
        business_name=data.get('business_name'),
        business_period=data.get('business_period'),
        amount=data.get('amount', 0),
        handler_id=data.get('handler_id'),
        remark=data.get('remark'),
        created_by=user_id
    )

    db.session.add(business)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '创建成功',
        'data': business.to_dict()
    })


@bp.route('/<int:business_id>', methods=['PUT'])
@jwt_required()
def update_business(business_id):
    """更新业务"""
    business = Business.query.get(business_id)

    if not business:
        return jsonify({'code': 404, 'message': '业务不存在'}), 404

    data = request.get_json()

    for key in ['business_type', 'business_name', 'business_period', 'amount',
                'handler_id', 'progress', 'remark']:
        if key in data:
            setattr(business, key, data[key])

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '更新成功',
        'data': business.to_dict()
    })


@bp.route('/<int:business_id>', methods=['DELETE'])
@jwt_required()
def delete_business(business_id):
    """删除业务"""
    business = Business.query.get(business_id)

    if not business:
        return jsonify({'code': 404, 'message': '业务不存在'}), 404

    db.session.delete(business)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '删除成功'
    })
