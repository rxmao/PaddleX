#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
财务模型
"""
from datetime import datetime
from app import db


class Payment(db.Model):
    """收款记录表"""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False, comment='客户ID')
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), comment='关联业务ID')
    payment_date = db.Column(db.Date, nullable=False, comment='收款日期')
    amount = db.Column(db.Decimal(10, 2), nullable=False, comment='收款金额')
    payment_method = db.Column(db.String(50), comment='支付方式')
    payment_account = db.Column(db.String(100), comment='收款账户')
    invoice_status = db.Column(db.String(20), default='pending', comment='发票状态')
    remark = db.Column(db.Text, comment='备注')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关联关系
    customer = db.relationship('Customer', backref='payments')
    business = db.relationship('Business', backref='payments')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.company_name if self.customer else None,
            'business_id': self.business_id,
            'payment_date': self.payment_date.strftime('%Y-%m-%d'),
            'amount': float(self.amount),
            'payment_method': self.payment_method,
            'payment_account': self.payment_account,
            'invoice_status': self.invoice_status,
            'remark': self.remark,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Invoice(db.Model):
    """发票记录表"""
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False, comment='客户ID')
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), comment='关联收款ID')
    invoice_type = db.Column(db.String(20), comment='发票类型')
    invoice_code = db.Column(db.String(50), comment='发票代码')
    invoice_number = db.Column(db.String(50), comment='发票号码')
    invoice_date = db.Column(db.Date, comment='开票日期')
    amount = db.Column(db.Decimal(10, 2), comment='发票金额')
    tax_amount = db.Column(db.Decimal(10, 2), comment='税额')
    remark = db.Column(db.Text, comment='备注')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关联关系
    customer = db.relationship('Customer', backref='invoices')
    payment = db.relationship('Payment', backref='invoices')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.company_name if self.customer else None,
            'payment_id': self.payment_id,
            'invoice_type': self.invoice_type,
            'invoice_code': self.invoice_code,
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date.strftime('%Y-%m-%d') if self.invoice_date else None,
            'amount': float(self.amount) if self.amount else 0,
            'tax_amount': float(self.tax_amount) if self.tax_amount else 0,
            'remark': self.remark,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
