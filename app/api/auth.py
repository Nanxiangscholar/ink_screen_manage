from . import api_bp
from flask import request, jsonify, session
from ..services.auth_service import AuthService
from ..utils.response import success_response, error_response
from ..utils.validators import AuthValidator


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json or {}
    
    # 验证输入
    is_valid, error_msg = AuthValidator.validate_login(data)
    if not is_valid:
        return error_response(error_msg)
    
    username = data.get('username')
    password = data.get('password')
    
    user, message = AuthService.login(username, password)
    if not user:
        return error_response(message)
    
    # 保存会话信息
    session['logged_in'] = True
    session['username'] = user.username
    session['role'] = user.role
    session['user_id'] = user.user_id
    
    return success_response({
        'username': user.username,
        'role': user.role,
        'user_id': user.user_id
    }, message)


@api_bp.route('/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json or {}
    
    # 验证输入
    is_valid, error_msg = AuthValidator.validate_register(data)
    if not is_valid:
        return error_response(error_msg)
    
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    user_id = data.get('user_id')
    invitation_code = data.get('invitation_code')
    
    user, message = AuthService.register(username, password, role, user_id, invitation_code)
    if not user:
        return error_response(message)
    
    return success_response({
        'username': user.username,
        'role': user.role,
        'user_id': user.user_id
    }, message)


@api_bp.route('/auth/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.clear()
    return success_response({}, '登出成功')
