#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
员工路由
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.employee import Employee

bp = Blueprint('employee', __name__)


@bp.route('', methods=['GET'])
@jwt_required()
def get_employees():
    """获取员工列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    department = request.args.get('department', '')
    status = request.args.get('status', '', type=str)

    query = Employee.query

    if department:
        query = query.filter_by(department=department)

    if status:
        query = query.filter_by(status=int(status))

    pagination = query.order_by(Employee.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'items': [employee.to_dict() for employee in pagination.items],
            'total': pagination.total
        }
    })


@bp.route('/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    """获取员工详情"""
    employee = Employee.query.get(employee_id)

    if not employee:
        return jsonify({'code': 404, 'message': '员工不存在'}), 404

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': employee.to_dict()
    })


@bp.route('', methods=['POST'])
@jwt_required()
def create_employee():
    """创建员工"""
    data = request.get_json()

    employee = Employee(
        user_id=data.get('user_id'),
        employee_no=data.get('employee_no'),
        department=data.get('department'),
        position=data.get('position'),
        base_salary=data.get('base_salary'),
        commission_rate=data.get('commission_rate'),
        remark=data.get('remark')
    )

    db.session.add(employee)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '创建成功',
        'data': employee.to_dict()
    })
