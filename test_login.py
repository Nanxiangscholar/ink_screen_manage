#!/usr/bin/env python3

from app import create_app
from app.models.base import db
from app.models.user import User
from app.services.auth_service import AuthService
from passlib.hash import pbkdf2_sha256
from sqlalchemy import text
from sqlalchemy import inspect

# 创建应用
app = create_app()

with app.app_context():
    try:
        # 检查数据库连接
        db.session.execute(text('SELECT 1'))
        print("数据库连接成功")
        
        # 删除现有的 user 表（如果存在）
        inspector = inspect(db.engine)
        if 'user' in inspector.get_table_names():
            print("删除现有的用户表...")
            User.__table__.drop(db.engine)
            print("用户表删除成功")
        
        # 创建新的 user 表
        print("创建用户表...")
        db.create_all()
        print("用户表创建成功")
        
        # 创建默认管理员用户
        print("创建默认管理员用户...")
        # 创建默认管理员用户，密码为 'admin123'
        hashed_password = pbkdf2_sha256.hash('admin123')
        admin_user = User(
            username='admin',
            password=hashed_password,
            role='admin',
            user_id='admin1'
        )
        db.session.add(admin_user)
        
        # 创建新用户 jushi1
        print("创建新用户 jushi1...")
        hashed_password_jushi1 = pbkdf2_sha256.hash('jushi1')
        jushi1_user = User(
            username='jushi1',
            password=hashed_password_jushi1,
            role='user',
            user_id='jushi1'
        )
        db.session.add(jushi1_user)
        
        # 提交所有更改
        db.session.commit()
        print("用户创建成功")
        
        # 测试登录
        print("\n测试 admin 登录...")
        user, message = AuthService.login('admin', 'admin123')
        if user:
            print(f"登录成功！用户: {user.username}, 角色: {user.role}")
        else:
            print(f"登录失败: {message}")
        
        print("\n测试 jushi1 登录...")
        user, message = AuthService.login('jushi1', 'jushi1')
        if user:
            print(f"登录成功！用户: {user.username}, 角色: {user.role}")
        else:
            print(f"登录失败: {message}")
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
