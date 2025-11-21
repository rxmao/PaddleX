#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
应用启动文件
"""
import os
from app import create_app

# 获取配置环境
config_name = os.environ.get('FLASK_ENV') or 'development'
app = create_app(config_name)

if __name__ == '__main__':
    # 开发环境运行
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
