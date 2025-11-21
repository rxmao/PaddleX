# 雅达管理（财税版）

## 项目简介

雅达管理（财税版）是专门为财税公司研发的内部管理软件，帮助财税公司高效管理客户、业务流程和财务数据。

**全国几乎所有省份都有我们的客户，免费试用，觉得确实对公司有帮助再付款！**

## 演示版本

- 演示地址：http://demo.yadaguanli.com/
- 账号：yadaguanli
- 密码：yd000000

## 核心功能模块

### 1. 客户管理
- 客户信息录入与维护
- 客户分类管理（一般纳税人/小规模纳税人）
- 客户跟进记录
- 客户合同管理
- 客户到期提醒

### 2. 业务管理
- **记账业务**：月度记账、季度记账
- **报税业务**：增值税、企业所得税、个人所得税
- **工商注册**：公司注册、变更、注销
- **资质办理**：各类资质证书办理
- 业务进度跟踪
- 业务到期自动提醒

### 3. 财务管理
- 收款管理（支持多种支付方式）
- 应收账款统计
- 发票管理（开票、收票）
- 财务报表生成
- 利润统计分析

### 4. 员工管理
- 员工信息管理
- 角色权限管理
- 工作量统计
- 绩效考核
- 提成计算

### 5. 统计分析
- 业务统计报表
- 客户分析（新增、流失、活跃度）
- 收入分析（月度、季度、年度）
- 员工业绩统计
- 数据可视化图表

### 6. 系统管理
- 用户管理
- 角色权限配置
- 系统参数设置
- 操作日志管理
- 数据备份

## 技术架构

### 前端技术栈
- **Vue 3**：渐进式JavaScript框架
- **Element Plus**：基于Vue 3的组件库
- **Pinia**：Vue状态管理
- **Vue Router**：路由管理
- **Axios**：HTTP请求
- **ECharts**：数据可视化
- **Vite**：构建工具

### 后端技术栈
- **Python 3.8+**：编程语言
- **Flask**：轻量级Web框架
- **Flask-SQLAlchemy**：ORM数据库操作
- **Flask-JWT-Extended**：JWT身份认证
- **MySQL**：关系型数据库
- **Redis**：缓存和会话管理
- **APScheduler**：定时任务

### 部署环境
- **Linux服务器**（推荐Ubuntu 20.04 / CentOS 7+）
- **Nginx**：反向代理和静态文件服务
- **Gunicorn**：WSGI服务器
- **Supervisor**：进程管理

## 项目结构

```
yada-management/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── api/             # API接口封装
│   │   ├── assets/          # 静态资源
│   │   ├── components/      # 公共组件
│   │   ├── views/           # 页面组件
│   │   ├── router/          # 路由配置
│   │   ├── store/           # 状态管理
│   │   ├── utils/           # 工具函数
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── backend/                  # 后端项目
│   ├── app/
│   │   ├── models/          # 数据模型
│   │   ├── routes/          # API路由
│   │   ├── services/        # 业务逻辑
│   │   ├── utils/           # 工具函数
│   │   └── __init__.py      # Flask应用工厂
│   ├── config.py            # 配置文件
│   ├── requirements.txt     # Python依赖
│   └── run.py              # 启动文件
├── database/                # 数据库
│   ├── schema.sql          # 数据库结构
│   └── init_data.sql       # 初始数据
├── deploy/                  # 部署配置
│   ├── nginx.conf          # Nginx配置
│   ├── supervisor.conf     # Supervisor配置
│   └── install.sh          # 安装脚本
└── docs/                    # 文档
    ├── API.md              # API文档
    ├── DEPLOY.md           # 部署文档
    └── USER_MANUAL.md      # 使用手册
```

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 5.7+
- Redis 5.0+（可选）

### 后端启动

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置数据库（编辑config.py）
vim config.py

# 初始化数据库
mysql -u root -p < ../database/schema.sql

# 启动服务
python run.py
```

后端将运行在：http://localhost:5000

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将运行在：http://localhost:3000

### 生产环境部署

详见：[部署文档](docs/DEPLOY.md)

```bash
# 使用一键安装脚本
cd deploy
chmod +x install.sh
sudo ./install.sh
```

## Linux服务器部署说明

### 支持的Linux发行版
- ✅ Ubuntu 18.04 / 20.04 / 22.04
- ✅ CentOS 7 / 8
- ✅ Debian 10 / 11
- ✅ Red Hat Enterprise Linux 7+

### 服务器最低配置
- CPU：2核
- 内存：4GB
- 硬盘：20GB
- 带宽：5Mbps

### 推荐配置
- CPU：4核
- 内存：8GB
- 硬盘：50GB SSD
- 带宽：10Mbps

## 功能特色

✨ **全流程管理**：从客户获取到业务完成的全流程跟踪
⏰ **智能提醒**：业务到期自动提醒，避免遗漏
📊 **多维度统计**：丰富的报表和数据分析功能
🔐 **权限管理**：灵活的角色权限配置
📱 **移动适配**：支持手机、平板访问
🚀 **高性能**：支持千级客户、万级业务数据
💾 **数据安全**：自动备份、操作日志完整

## 默认账号

- 管理员账号：admin
- 默认密码：admin123

**首次登录后请立即修改密码！**

## 技术支持

- 文档：查看 `docs/` 目录
- 问题反馈：提交 Issue
- 商务合作：联系客服

## 开源协议

本项目采用 MIT 协议开源

## 联系我们

**免费试用，觉得确实对公司有帮助再付款！**

试用申请请访问：http://demo.yadaguanli.com/
