from . import api_bp
from flask import request, jsonify, session
from ..services.user_service import UserService
from ..utils.response import success_response, error_response
from ..utils.decorators import login_required


@api_bp.route('/user/info', methods=['GET'])
@login_required

def get_user_info():
    """获取用户信息"""
    user_id = session.get('user_id')
    user = UserService.get_user_by_id(user_id)
    
    if not user:
        return error_response('用户不存在')
    
    return success_response({
        'username': user.username,
        'role': user.role,
        'user_id': user.user_id
    })


@api_bp.route('/user/password', methods=['PUT'])
@login_required

def update_password():
    """更新密码"""
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return error_response('缺少必要参数')
    
    user_id = session.get('user_id')
    user = UserService.get_user_by_id(user_id)
    
    if not user:
        return error_response('用户不存在')
    
    success, message = UserService.update_password(user, old_password, new_password)
    if not success:
        return error_response(message)
    
    return success_response({}, message)
