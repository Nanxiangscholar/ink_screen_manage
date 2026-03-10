from flask import session, jsonify
from functools import wraps


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({
                'success': False,
                'data': None,
                'message': '请先登录'
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def permission_required(required_role):
    """权限验证装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return jsonify({
                    'success': False,
                    'data': None,
                    'message': '请先登录'
                }), 401
            
            user_role = session.get('role')
            if user_role != required_role and user_role != 'admin':
                return jsonify({
                    'success': False,
                    'data': None,
                    'message': '权限不足'
                }), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
