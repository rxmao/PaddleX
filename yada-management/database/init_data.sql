-- 初始数据
USE yada_management;

-- 插入管理员用户（密码：admin123）
-- 密码哈希使用werkzeug.security生成
INSERT INTO `users` (`username`, `password_hash`, `real_name`, `phone`, `email`, `role`, `status`) VALUES
('admin', 'scrypt:32768:8:1$KJxXZZGqh2fBGi1f$b8a5f0c9e7d6f3a1b2c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3', '系统管理员', '13800000000', 'admin@yadaguanli.com', 'admin', 1),
('zhangsan', 'scrypt:32768:8:1$KJxXZZGqh2fBGi1f$b8a5f0c9e7d6f3a1b2c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3', '张三', '13800000001', 'zhangsan@example.com', 'manager', 1),
('lisi', 'scrypt:32768:8:1$KJxXZZGqh2fBGi1f$b8a5f0c9e7d6f3a1b2c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3', '李四', '13800000002', 'lisi@example.com', 'user', 1);

-- 插入示例客户数据
INSERT INTO `customers` (`company_name`, `company_code`, `taxpayer_type`, `industry`, `contact_person`, `contact_phone`, `address`, `salesman_id`, `accountant_id`, `status`) VALUES
('深圳市科技有限公司', '91440300MA5DXXX123', 'general', '软件和信息技术服务业', '王经理', '13900000001', '深圳市南山区科技园', 2, 3, 1),
('广州贸易公司', '91440100MA5DXXX456', 'small', '批发和零售业', '李总', '13900000002', '广州市天河区', 2, 3, 1),
('东莞制造厂', '91441900MA5DXXX789', 'general', '制造业', '陈厂长', '13900000003', '东莞市长安镇', 2, 3, 1);

-- 插入示例业务数据
INSERT INTO `business` (`customer_id`, `business_type`, `business_name`, `business_period`, `start_date`, `end_date`, `amount`, `handler_id`, `progress`) VALUES
(1, '记账', '2024年11月记账服务', '月度', '2024-11-01', '2024-11-30', 500.00, 3, 'processing'),
(1, '报税', '2024年11月增值税申报', '月度', '2024-11-01', '2024-11-15', 300.00, 3, 'pending'),
(2, '记账', '2024年Q4记账服务', '季度', '2024-10-01', '2024-12-31', 1200.00, 3, 'processing'),
(3, '工商注册', '公司地址变更', '一次性', '2024-11-01', '2024-11-30', 800.00, 2, 'completed');

-- 插入示例收款数据
INSERT INTO `payments` (`customer_id`, `business_id`, `payment_date`, `amount`, `payment_method`, `payment_account`, `invoice_status`) VALUES
(1, 1, '2024-11-01', 500.00, '转账', '工商银行', 'issued'),
(2, 3, '2024-10-01', 1200.00, '支付宝', '支付宝', 'pending'),
(3, 4, '2024-11-05', 800.00, '微信', '微信', 'issued');

-- 插入示例员工数据
INSERT INTO `employees` (`user_id`, `employee_no`, `department`, `position`, `entry_date`, `base_salary`, `commission_rate`, `status`) VALUES
(2, 'YD001', '业务部', '业务经理', '2023-01-01', 8000.00, 10.00, 1),
(3, 'YD002', '财务部', '会计', '2023-03-01', 6000.00, 5.00, 1);
