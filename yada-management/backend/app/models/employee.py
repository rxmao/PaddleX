#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
员工模型
"""
from datetime import datetime
from app import db


class Employee(db.Model):
    """员工表"""
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, comment='关联用户ID')
    employee_no = db.Column(db.String(50), unique=True, comment='员工工号')
    department = db.Column(db.String(50), comment='部门')
    position = db.Column(db.String(50), comment='职位')
    entry_date = db.Column(db.Date, comment='入职日期')
    leave_date = db.Column(db.Date, comment='离职日期')
    base_salary = db.Column(db.Decimal(10, 2), comment='基本工资')
    commission_rate = db.Column(db.Decimal(5, 2), comment='提成比例')
    status = db.Column(db.Integer, default=1, comment='状态：1在职 0离职')
    remark = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关联关系
    user = db.relationship('User', backref='employee_info')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'real_name': self.user.real_name if self.user else None,
            'phone': self.user.phone if self.user else None,
            'employee_no': self.employee_no,
            'department': self.department,
            'position': self.position,
            'entry_date': self.entry_date.strftime('%Y-%m-%d') if self.entry_date else None,
            'leave_date': self.leave_date.strftime('%Y-%m-%d') if self.leave_date else None,
            'base_salary': float(self.base_salary) if self.base_salary else 0,
            'commission_rate': float(self.commission_rate) if self.commission_rate else 0,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
