#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
业务模型
"""
from datetime import datetime
from app import db


class Business(db.Model):
    """业务表"""
    __tablename__ = 'business'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False, comment='客户ID')
    business_type = db.Column(db.String(50), nullable=False, comment='业务类型')
    business_name = db.Column(db.String(200), nullable=False, comment='业务名称')
    business_period = db.Column(db.String(50), comment='业务周期：月度/季度/年度')
    start_date = db.Column(db.Date, comment='开始日期')
    end_date = db.Column(db.Date, comment='结束日期')
    amount = db.Column(db.Decimal(10, 2), default=0, comment='业务金额')
    handler_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='经办人ID')
    progress = db.Column(db.String(20), default='pending', comment='进度：pending/processing/completed/cancelled')
    remind_days = db.Column(db.Integer, default=3, comment='提前提醒天数')
    remark = db.Column(db.Text, comment='备注')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关联关系
    customer = db.relationship('Customer', backref='businesses')
    handler = db.relationship('User', foreign_keys=[handler_id], backref='handled_businesses')

    def to_dict(self):
        """转换为字典"""
        progress_dict = {
            'pending': '待处理',
            'processing': '处理中',
            'completed': '已完成',
            'cancelled': '已取消'
        }
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.company_name if self.customer else None,
            'business_type': self.business_type,
            'business_name': self.business_name,
            'business_period': self.business_period,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'amount': float(self.amount) if self.amount else 0,
            'handler_id': self.handler_id,
            'handler_name': self.handler.real_name if self.handler else None,
            'progress': self.progress,
            'progress_text': progress_dict.get(self.progress, '未知'),
            'remind_days': self.remind_days,
            'remark': self.remark,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
