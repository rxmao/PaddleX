#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
统计分析路由
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from app import db
from app.models.customer import Customer
from app.models.business import Business
from app.models.finance import Payment

bp = Blueprint('statistics', __name__)


@bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """获取工作台统计数据"""
    # 客户总数
    total_customers = Customer.query.filter_by(status=1).count()

    # 进行中的业务
    processing_business = Business.query.filter_by(progress='processing').count()

    # 本月收款金额
    from datetime import datetime
    current_month = datetime.now().month
    current_year = datetime.now().year

    monthly_payment = db.session.query(func.sum(Payment.amount)).filter(
        func.year(Payment.payment_date) == current_year,
        func.month(Payment.payment_date) == current_month
    ).scalar() or 0

    # 待处理业务
    pending_business = Business.query.filter_by(progress='pending').count()

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'total_customers': total_customers,
            'processing_business': processing_business,
            'monthly_payment': float(monthly_payment),
            'pending_business': pending_business
        }
    })


@bp.route('/business-chart', methods=['GET'])
@jwt_required()
def get_business_chart():
    """获取业务统计图表数据"""
    # 按业务类型统计
    business_stats = db.session.query(
        Business.business_type,
        func.count(Business.id).label('count')
    ).group_by(Business.business_type).all()

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': [
            {'type': stat[0], 'count': stat[1]}
            for stat in business_stats
        ]
    })
