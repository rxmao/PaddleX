#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
财务路由
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.finance import Payment, Invoice

bp = Blueprint('finance', __name__)


@bp.route('/payments', methods=['GET'])
@jwt_required()
def get_payments():
    """获取收款列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = Payment.query.order_by(Payment.payment_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'items': [payment.to_dict() for payment in pagination.items],
            'total': pagination.total
        }
    })


@bp.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    """创建收款记录"""
    user_id = get_jwt_identity()
    data = request.get_json()

    payment = Payment(
        customer_id=data.get('customer_id'),
        business_id=data.get('business_id'),
        payment_date=data.get('payment_date'),
        amount=data.get('amount'),
        payment_method=data.get('payment_method'),
        payment_account=data.get('payment_account'),
        remark=data.get('remark'),
        created_by=user_id
    )

    db.session.add(payment)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '创建成功',
        'data': payment.to_dict()
    })


@bp.route('/invoices', methods=['GET'])
@jwt_required()
def get_invoices():
    """获取发票列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    pagination = Invoice.query.order_by(Invoice.invoice_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'items': [invoice.to_dict() for invoice in pagination.items],
            'total': pagination.total
        }
    })


@bp.route('/invoices', methods=['POST'])
@jwt_required()
def create_invoice():
    """创建发票记录"""
    user_id = get_jwt_identity()
    data = request.get_json()

    invoice = Invoice(
        customer_id=data.get('customer_id'),
        payment_id=data.get('payment_id'),
        invoice_type=data.get('invoice_type'),
        invoice_code=data.get('invoice_code'),
        invoice_number=data.get('invoice_number'),
        invoice_date=data.get('invoice_date'),
        amount=data.get('amount'),
        tax_amount=data.get('tax_amount'),
        remark=data.get('remark'),
        created_by=user_id
    )

    db.session.add(invoice)
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '创建成功',
        'data': invoice.to_dict()
    })
