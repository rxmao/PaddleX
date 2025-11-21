#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
客户路由
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.customer import Customer

bp = Blueprint('customer', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_customers():
    """获取客户列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    keyword = request.args.get('keyword', '')
    taxpayer_type = request.args.get('taxpayer_type', '')
    status = request.args.get('status', '', type=str)

    query = Customer.query

    # 搜索过滤
    if keyword:
        query = query.filter(
            db.or_(
                Customer.company_name.like(f'%{keyword}%'),
                Customer.contact_person.like(f'%{keyword}%'),
                Customer.contact_phone.like(f'%{keyword}%')
            )
        )

    if taxpayer_type:
        query = query.filter_by(taxpayer_type=taxpayer_type)

    if status:
        query = query.filter_by(status=int(status))

    # 分页
    pagination = query.order_by(Customer.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'items': [customer.to_dict() for customer in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page
        }
    })


@bp.route('/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    """获取客户详情"""
    customer = Customer.query.get(customer_id)

    if not customer:
        return jsonify({'code': 404, 'message': '客户不存在'}), 404

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': customer.to_dict()
    })


@bp.route('', methods=['POST'])
@jwt_required()
def create_customer():
    """创建客户"""
    user_id = get_jwt_identity()
    data = request.get_json()

    # 检查公司名称是否已存在
    if Customer.query.filter_by(company_name=data.get('company_name')).first():
        return jsonify({'code': 400, 'message': '公司名称已存在'}), 400

    customer = Customer(
        company_name=data.get('company_name'),
        company_code=data.get('company_code'),
        taxpayer_type=data.get('taxpayer_type'),
        industry=data.get('industry'),
        contact_person=data.get('contact_person'),
        contact_phone=data.get('contact_phone'),
        contact_email=data.get('contact_email'),
        address=data.get('address'),
        business_scope=data.get('business_scope'),
        salesman_id=data.get('salesman_id'),
        accountant_id=data.get('accountant_id'),
        remark=data.get('remark'),
        created_by=user_id
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '创建成功',
        'data': customer.to_dict()
    })


@bp.route('/<int:customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    """更新客户"""
    customer = Customer.query.get(customer_id)

    if not customer:
        return jsonify({'code': 404, 'message': '客户不存在'}), 404

    data = request.get_json()

    # 更新字段
    for key in ['company_name', 'company_code', 'taxpayer_type', 'industry',
                'contact_person', 'contact_phone', 'contact_email', 'address',
                'business_scope', 'salesman_id', 'accountant_id', 'status', 'remark']:
        if key in data:
            setattr(customer, key, data[key])

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '更新成功',
        'data': customer.to_dict()
    })


@bp.route('/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    """删除客户"""
    customer = Customer.query.get(customer_id)

    if not customer:
        return jsonify({'code': 404, 'message': '客户不存在'}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '删除成功'
    })
