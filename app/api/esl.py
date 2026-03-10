from . import api_bp
from flask import request, session
from ..services.esl_service import get_esl_service
from ..utils.response import success_response, error_response
from ..utils.decorators import login_required
from ..utils.validators import ESLValidator
from ..utils.logger import logger


@api_bp.route('/esl/goods', methods=['GET'])
@login_required
def get_esl_goods():
    """获取电子标签商品绑定信息"""
    sku = request.args.get('sku', '').strip()
    esl_id = request.args.get('esl_id', '').strip()
    
    try:
        goods = get_esl_service().get_esl_goods(sku, esl_id)
        return success_response(goods)
    except Exception as e:
        logger.error(f"获取ESL商品绑定信息失败: {str(e)}")
        return error_response('获取绑定信息失败')


@api_bp.route('/esl/bind', methods=['POST'])
@login_required
def bind_label():
    """绑定标签到商品"""
    data = request.json or {}
    
    # 验证输入
    is_valid, error_msg = ESLValidator.validate_bind(data)
    if not is_valid:
        return error_response(error_msg)
    
    esl_id = data.get('esl_id')
    sku = data.get('sku')
    
    try:
        success, message = get_esl_service().bind_label(esl_id, sku)
        if not success:
            return error_response(message)
        return success_response({}, message)
    except Exception as e:
        logger.error(f"绑定标签失败: {str(e)}")
        return error_response('绑定标签失败')


@api_bp.route('/esl/unbind', methods=['POST'])
@login_required
def unbind_label():
    """解绑标签"""
    data = request.json or {}
    
    # 验证输入
    is_valid, error_msg = ESLValidator.validate_bind(data)
    if not is_valid:
        return error_response(error_msg)
    
    esl_id = data.get('esl_id')
    sku = data.get('sku')
    
    try:
        success, message = get_esl_service().unbind_label(esl_id, sku)
        if not success:
            return error_response(message)
        return success_response({}, message)
    except Exception as e:
        logger.error(f"解绑标签失败: {str(e)}")
        return error_response('解绑标签失败')


@api_bp.route('/esl/ids', methods=['GET'])
@login_required
def get_esl_ids():
    """获取所有电子标签 ID"""
    try:
        esl_ids = get_esl_service().get_esl_ids()
        return success_response(esl_ids)
    except Exception as e:
        logger.error(f"获取ESL ID列表失败: {str(e)}")
        return error_response('获取ESL ID列表失败')


@api_bp.route('/esl/skus', methods=['GET'])
@login_required
def get_skus():
    """根据角色获取 SKU 列表"""
    user_role = session.get('role', 'user')
    try:
        skus = get_esl_service().get_skus(user_role)
        return success_response(skus)
    except Exception as e:
        logger.error(f"获取SKU列表失败: {str(e)}")
        return error_response('获取SKU列表失败')


@api_bp.route('/esl/status', methods=['POST'])
@login_required
def get_esl_status():
    """批量获取标签状态"""
    data = request.json or {}
    esl_ids = data.get('esl_ids', [])
    
    # 验证输入
    is_valid, error_msg = ESLValidator.validate_esl_ids(esl_ids)
    if not is_valid:
        return error_response(error_msg)
    
    try:
        status = get_esl_service().get_esl_status(esl_ids)
        return success_response(status)
    except Exception as e:
        logger.error(f"获取标签状态失败: {str(e)}")
        return error_response('获取标签状态失败')
