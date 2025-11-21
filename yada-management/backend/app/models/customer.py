#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
客户模型
"""
from datetime import datetime
from app import db


class Customer(db.Model):
    """客户表"""
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False, comment='公司名称')
    company_code = db.Column(db.String(50), unique=True, comment='统一社会信用代码')
    taxpayer_type = db.Column(db.String(20), comment='纳税人类型：general/small')
    industry = db.Column(db.String(100), comment='所属行业')
    contact_person = db.Column(db.String(50), comment='联系人')
    contact_phone = db.Column(db.String(20), comment='联系电话')
    contact_email = db.Column(db.String(100), comment='联系邮箱')
    address = db.Column(db.String(255), comment='公司地址')
    business_scope = db.Column(db.Text, comment='经营范围')
    registration_date = db.Column(db.Date, comment='注册日期')
    service_start_date = db.Column(db.Date, comment='服务开始日期')
    salesman_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='业务员ID')
    accountant_id = db.Column(db.Integer, db.ForeignKey('users.id'), comment='会计ID')
    status = db.Column(db.Integer, default=1, comment='状态：1正常 0停用')
    remark = db.Column(db.Text, comment='备注')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), comment='创建人')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')

    # 关联关系
    salesman = db.relationship('User', foreign_keys=[salesman_id], backref='customers_as_salesman')
    accountant = db.relationship('User', foreign_keys=[accountant_id], backref='customers_as_accountant')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'company_name': self.company_name,
            'company_code': self.company_code,
            'taxpayer_type': self.taxpayer_type,
            'taxpayer_type_text': '一般纳税人' if self.taxpayer_type == 'general' else '小规模纳税人',
            'industry': self.industry,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email,
            'address': self.address,
            'business_scope': self.business_scope,
            'registration_date': self.registration_date.strftime('%Y-%m-%d') if self.registration_date else None,
            'service_start_date': self.service_start_date.strftime('%Y-%m-%d') if self.service_start_date else None,
            'salesman_id': self.salesman_id,
            'salesman_name': self.salesman.real_name if self.salesman else None,
            'accountant_id': self.accountant_id,
            'accountant_name': self.accountant.real_name if self.accountant else None,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
