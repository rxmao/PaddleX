# 部署文档

## Linux服务器部署指南

本文档详细介绍如何在Linux服务器上部署雅达管理（财税版）系统。

### 一、系统要求

#### 支持的操作系统
- Ubuntu 18.04 / 20.04 / 22.04
- CentOS 7 / 8
- Debian 10 / 11
- Red Hat Enterprise Linux 7+

#### 最低配置
- CPU: 2核
- 内存: 4GB
- 硬盘: 20GB
- 带宽: 5Mbps

#### 推荐配置
- CPU: 4核
- 内存: 8GB
- 硬盘: 50GB SSD
- 带宽: 10Mbps

### 二、环境准备

#### 1. 更新系统

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt upgrade -y
```

**CentOS/RHEL:**
```bash
sudo yum update -y
```

#### 2. 安装Python 3.8+

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip python3-venv -y
```

**CentOS/RHEL:**
```bash
sudo yum install python3 python3-pip -y
```

验证安装:
```bash
python3 --version
```

#### 3. 安装MySQL 5.7+

**Ubuntu/Debian:**
```bash
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql
sudo mysql_secure_installation
```

**CentOS/RHEL:**
```bash
sudo yum install mysql-server -y
sudo systemctl start mysqld
sudo systemctl enable mysqld
sudo mysql_secure_installation
```

#### 4. 安装Node.js 16+

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs  # Ubuntu/Debian
# 或
sudo yum install -y nodejs  # CentOS/RHEL
```

验证安装:
```bash
node --version
npm --version
```

#### 5. 安装Nginx

**Ubuntu/Debian:**
```bash
sudo apt install nginx -y
```

**CentOS/RHEL:**
```bash
sudo yum install nginx -y
```

启动Nginx:
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### 6. 安装Redis（可选）

**Ubuntu/Debian:**
```bash
sudo apt install redis-server -y
sudo systemctl start redis
sudo systemctl enable redis
```

**CentOS/RHEL:**
```bash
sudo yum install redis -y
sudo systemctl start redis
sudo systemctl enable redis
```

### 三、部署步骤

#### 1. 创建项目目录

```bash
sudo mkdir -p /var/www/yada-management
sudo chown -R $USER:$USER /var/www/yada-management
cd /var/www/yada-management
```

#### 2. 克隆代码

```bash
git clone <your-repo-url> .
```

#### 3. 配置数据库

登录MySQL:
```bash
mysql -u root -p
```

创建数据库和用户:
```sql
CREATE DATABASE yada_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'yadauser'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON yada_management.* TO 'yadauser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

导入数据库结构:
```bash
mysql -u yadauser -p yada_management < database/schema.sql
mysql -u yadauser -p yada_management < database/init_data.sql
```

#### 4. 部署后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制配置文件
cp .env.example .env

# 编辑配置文件
nano .env
```

修改`.env`文件中的数据库配置:
```env
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=yadauser
MYSQL_PASSWORD=your_strong_password
MYSQL_DATABASE=yada_management
JWT_SECRET_KEY=your-jwt-secret-key
```

测试后端:
```bash
python run.py
# 确认能正常启动后按Ctrl+C停止
```

#### 5. 安装Gunicorn

```bash
pip install gunicorn
```

#### 6. 部署前端

```bash
cd ../frontend

# 安装依赖
npm install

# 构建生产版本
npm run build
```

#### 7. 配置Nginx

创建Nginx配置文件:
```bash
sudo nano /etc/nginx/sites-available/yada-management
```

添加以下内容:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # 修改为你的域名或IP

    # 前端静态文件
    location / {
        root /var/www/yada-management/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件缓存
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

启用配置:
```bash
sudo ln -s /etc/nginx/sites-available/yada-management /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置
sudo systemctl reload nginx
```

#### 8. 配置Supervisor

安装Supervisor:
```bash
sudo apt install supervisor -y  # Ubuntu/Debian
# 或
sudo yum install supervisor -y  # CentOS/RHEL
```

创建Supervisor配置:
```bash
sudo nano /etc/supervisor/conf.d/yada-management.conf
```

添加以下内容:
```ini
[program:yada-backend]
directory=/var/www/yada-management/backend
command=/var/www/yada-management/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 run:app
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/yada-backend.err.log
stdout_logfile=/var/log/yada-backend.out.log
```

启动服务:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start yada-backend
sudo supervisorctl status
```

### 四、配置HTTPS（推荐）

#### 使用Let's Encrypt免费SSL证书

```bash
# 安装certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### 五、维护操作

#### 查看日志

```bash
# 后端日志
sudo tail -f /var/log/yada-backend.out.log
sudo tail -f /var/log/yada-backend.err.log

# Nginx日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### 重启服务

```bash
# 重启后端
sudo supervisorctl restart yada-backend

# 重启Nginx
sudo systemctl restart nginx
```

#### 更新代码

```bash
cd /var/www/yada-management

# 拉取最新代码
git pull

# 更新后端
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart yada-backend

# 更新前端
cd ../frontend
npm install
npm run build
sudo systemctl reload nginx
```

#### 数据库备份

```bash
# 备份
mysqldump -u yadauser -p yada_management > backup_$(date +%Y%m%d).sql

# 恢复
mysql -u yadauser -p yada_management < backup_20241121.sql
```

### 六、安全建议

1. **防火墙配置**
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

2. **定期更新系统**
```bash
sudo apt update && sudo apt upgrade -y
```

3. **使用强密码**
   - 数据库密码
   - SECRET_KEY
   - JWT_SECRET_KEY

4. **限制SSH访问**
   - 禁用root登录
   - 使用SSH密钥认证

5. **定期备份数据库**
   - 建议每天自动备份
   - 异地存储备份文件

### 七、故障排查

#### 后端无法启动

```bash
# 查看日志
sudo tail -f /var/log/yada-backend.err.log

# 检查端口占用
sudo netstat -tlnp | grep 5000

# 手动测试
cd /var/www/yada-management/backend
source venv/bin/activate
python run.py
```

#### 前端页面空白

```bash
# 检查Nginx配置
sudo nginx -t

# 检查文件权限
ls -l /var/www/yada-management/frontend/dist

# 查看Nginx错误日志
sudo tail -f /var/log/nginx/error.log
```

#### 数据库连接失败

```bash
# 检查MySQL服务
sudo systemctl status mysql

# 测试连接
mysql -u yadauser -p yada_management

# 检查防火墙
sudo ufw status
```

### 八、性能优化

1. **启用Gzip压缩**（Nginx配置）
2. **使用Redis缓存**
3. **配置数据库索引**
4. **使用CDN加速静态资源**
5. **增加Gunicorn worker数量**

### 九、监控建议

1. 使用Prometheus + Grafana监控系统资源
2. 配置日志收集（ELK Stack）
3. 设置告警通知
4. 定期检查系统性能

## 联系支持

如有问题，请联系技术支持。
