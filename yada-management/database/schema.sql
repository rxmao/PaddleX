-- 雅达管理（财税版）数据库结构
-- MySQL 5.7+

-- 创建数据库
CREATE DATABASE IF NOT EXISTS yada_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE yada_management;

-- 用户表
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` VARCHAR(50) NOT NULL COMMENT '用户名',
  `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
  `real_name` VARCHAR(50) DEFAULT NULL COMMENT '真实姓名',
  `phone` VARCHAR(20) DEFAULT NULL COMMENT '手机号',
  `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
  `role` VARCHAR(20) DEFAULT 'user' COMMENT '角色：admin/manager/user',
  `status` TINYINT(1) DEFAULT 1 COMMENT '状态：1启用 0禁用',
  `last_login` DATETIME DEFAULT NULL COMMENT '最后登录时间',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_username` (`username`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 客户表
CREATE TABLE IF NOT EXISTS `customers` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '客户ID',
  `company_name` VARCHAR(200) NOT NULL COMMENT '公司名称',
  `company_code` VARCHAR(50) DEFAULT NULL COMMENT '统一社会信用代码',
  `taxpayer_type` VARCHAR(20) DEFAULT NULL COMMENT '纳税人类型：general一般纳税人/small小规模纳税人',
  `industry` VARCHAR(100) DEFAULT NULL COMMENT '所属行业',
  `contact_person` VARCHAR(50) DEFAULT NULL COMMENT '联系人',
  `contact_phone` VARCHAR(20) DEFAULT NULL COMMENT '联系电话',
  `contact_email` VARCHAR(100) DEFAULT NULL COMMENT '联系邮箱',
  `address` VARCHAR(255) DEFAULT NULL COMMENT '公司地址',
  `business_scope` TEXT DEFAULT NULL COMMENT '经营范围',
  `registration_date` DATE DEFAULT NULL COMMENT '注册日期',
  `service_start_date` DATE DEFAULT NULL COMMENT '服务开始日期',
  `salesman_id` INT(11) DEFAULT NULL COMMENT '业务员ID',
  `accountant_id` INT(11) DEFAULT NULL COMMENT '会计ID',
  `status` TINYINT(1) DEFAULT 1 COMMENT '状态：1正常 0停用',
  `remark` TEXT DEFAULT NULL COMMENT '备注',
  `created_by` INT(11) DEFAULT NULL COMMENT '创建人',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_company_code` (`company_code`),
  KEY `idx_company_name` (`company_name`),
  KEY `idx_taxpayer_type` (`taxpayer_type`),
  KEY `idx_salesman` (`salesman_id`),
  KEY `idx_accountant` (`accountant_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_customers_salesman` FOREIGN KEY (`salesman_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_customers_accountant` FOREIGN KEY (`accountant_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_customers_creator` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户表';

-- 业务表
CREATE TABLE IF NOT EXISTS `business` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '业务ID',
  `customer_id` INT(11) NOT NULL COMMENT '客户ID',
  `business_type` VARCHAR(50) NOT NULL COMMENT '业务类型：记账/报税/工商注册/资质办理',
  `business_name` VARCHAR(200) NOT NULL COMMENT '业务名称',
  `business_period` VARCHAR(50) DEFAULT NULL COMMENT '业务周期：月度/季度/年度',
  `start_date` DATE DEFAULT NULL COMMENT '开始日期',
  `end_date` DATE DEFAULT NULL COMMENT '结束日期',
  `amount` DECIMAL(10,2) DEFAULT 0.00 COMMENT '业务金额',
  `handler_id` INT(11) DEFAULT NULL COMMENT '经办人ID',
  `progress` VARCHAR(20) DEFAULT 'pending' COMMENT '进度：pending待处理/processing处理中/completed已完成/cancelled已取消',
  `remind_days` INT(3) DEFAULT 3 COMMENT '提前提醒天数',
  `remark` TEXT DEFAULT NULL COMMENT '备注',
  `created_by` INT(11) DEFAULT NULL COMMENT '创建人',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_customer` (`customer_id`),
  KEY `idx_business_type` (`business_type`),
  KEY `idx_progress` (`progress`),
  KEY `idx_handler` (`handler_id`),
  KEY `idx_end_date` (`end_date`),
  CONSTRAINT `fk_business_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_business_handler` FOREIGN KEY (`handler_id`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_business_creator` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='业务表';

-- 收款记录表
CREATE TABLE IF NOT EXISTS `payments` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '收款ID',
  `customer_id` INT(11) NOT NULL COMMENT '客户ID',
  `business_id` INT(11) DEFAULT NULL COMMENT '关联业务ID',
  `payment_date` DATE NOT NULL COMMENT '收款日期',
  `amount` DECIMAL(10,2) NOT NULL COMMENT '收款金额',
  `payment_method` VARCHAR(50) DEFAULT NULL COMMENT '支付方式：现金/转账/支付宝/微信',
  `payment_account` VARCHAR(100) DEFAULT NULL COMMENT '收款账户',
  `invoice_status` VARCHAR(20) DEFAULT 'pending' COMMENT '发票状态：pending待开/issued已开',
  `remark` TEXT DEFAULT NULL COMMENT '备注',
  `created_by` INT(11) DEFAULT NULL COMMENT '创建人',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_customer` (`customer_id`),
  KEY `idx_business` (`business_id`),
  KEY `idx_payment_date` (`payment_date`),
  CONSTRAINT `fk_payments_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_payments_business` FOREIGN KEY (`business_id`) REFERENCES `business` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_payments_creator` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='收款记录表';

-- 发票记录表
CREATE TABLE IF NOT EXISTS `invoices` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '发票ID',
  `customer_id` INT(11) NOT NULL COMMENT '客户ID',
  `payment_id` INT(11) DEFAULT NULL COMMENT '关联收款ID',
  `invoice_type` VARCHAR(20) DEFAULT NULL COMMENT '发票类型：普通发票/增值税专用发票',
  `invoice_code` VARCHAR(50) DEFAULT NULL COMMENT '发票代码',
  `invoice_number` VARCHAR(50) DEFAULT NULL COMMENT '发票号码',
  `invoice_date` DATE DEFAULT NULL COMMENT '开票日期',
  `amount` DECIMAL(10,2) DEFAULT 0.00 COMMENT '发票金额',
  `tax_amount` DECIMAL(10,2) DEFAULT 0.00 COMMENT '税额',
  `remark` TEXT DEFAULT NULL COMMENT '备注',
  `created_by` INT(11) DEFAULT NULL COMMENT '创建人',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_customer` (`customer_id`),
  KEY `idx_payment` (`payment_id`),
  KEY `idx_invoice_date` (`invoice_date`),
  CONSTRAINT `fk_invoices_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_invoices_payment` FOREIGN KEY (`payment_id`) REFERENCES `payments` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_invoices_creator` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='发票记录表';

-- 员工表
CREATE TABLE IF NOT EXISTS `employees` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '员工ID',
  `user_id` INT(11) DEFAULT NULL COMMENT '关联用户ID',
  `employee_no` VARCHAR(50) DEFAULT NULL COMMENT '员工工号',
  `department` VARCHAR(50) DEFAULT NULL COMMENT '部门',
  `position` VARCHAR(50) DEFAULT NULL COMMENT '职位',
  `entry_date` DATE DEFAULT NULL COMMENT '入职日期',
  `leave_date` DATE DEFAULT NULL COMMENT '离职日期',
  `base_salary` DECIMAL(10,2) DEFAULT 0.00 COMMENT '基本工资',
  `commission_rate` DECIMAL(5,2) DEFAULT 0.00 COMMENT '提成比例',
  `status` TINYINT(1) DEFAULT 1 COMMENT '状态：1在职 0离职',
  `remark` TEXT DEFAULT NULL COMMENT '备注',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_user_id` (`user_id`),
  UNIQUE KEY `idx_employee_no` (`employee_no`),
  KEY `idx_department` (`department`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_employees_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工表';

-- 操作日志表
CREATE TABLE IF NOT EXISTS `operation_logs` (
  `id` INT(11) NOT NULL AUTO_INCREMENT COMMENT '日志ID',
  `user_id` INT(11) DEFAULT NULL COMMENT '操作用户ID',
  `module` VARCHAR(50) DEFAULT NULL COMMENT '操作模块',
  `action` VARCHAR(50) DEFAULT NULL COMMENT '操作动作',
  `content` TEXT DEFAULT NULL COMMENT '操作内容',
  `ip_address` VARCHAR(50) DEFAULT NULL COMMENT 'IP地址',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '操作时间',
  PRIMARY KEY (`id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_module` (`module`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `fk_logs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志表';
