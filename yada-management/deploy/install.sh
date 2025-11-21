#!/bin/bash
# 雅达管理系统一键部署脚本
# 适用于Ubuntu 20.04+

set -e

echo "===================================="
echo "雅达管理（财税版）一键部署脚本"
echo "===================================="
echo ""

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
  echo "请使用sudo运行此脚本"
  exit 1
fi

# 检查操作系统
if [ ! -f /etc/os-release ]; then
  echo "不支持的操作系统"
  exit 1
fi

source /etc/os-release

echo "检测到操作系统: $PRETTY_NAME"
echo ""

# 更新系统
echo "[1/8] 更新系统..."
apt update && apt upgrade -y

# 安装Python
echo "[2/8] 安装Python 3..."
apt install python3 python3-pip python3-venv -y

# 安装MySQL
echo "[3/8] 安装MySQL..."
apt install mysql-server -y
systemctl start mysql
systemctl enable mysql

# 安装Node.js
echo "[4/8] 安装Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# 安装Nginx
echo "[5/8] 安装Nginx..."
apt install nginx -y
systemctl start nginx
systemctl enable nginx

# 安装Redis
echo "[6/8] 安装Redis..."
apt install redis-server -y
systemctl start redis
systemctl enable redis

# 安装Supervisor
echo "[7/8] 安装Supervisor..."
apt install supervisor -y
systemctl start supervisor
systemctl enable supervisor

# 配置防火墙
echo "[8/8] 配置防火墙..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
echo "y" | ufw enable

echo ""
echo "===================================="
echo "基础环境安装完成！"
echo "===================================="
echo ""
echo "接下来请手动执行以下步骤："
echo "1. 配置MySQL数据库"
echo "2. 克隆项目代码"
echo "3. 配置后端环境"
echo "4. 构建前端"
echo "5. 配置Nginx和Supervisor"
echo ""
echo "详细步骤请参考: docs/DEPLOY.md"
