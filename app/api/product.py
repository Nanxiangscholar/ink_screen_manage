from . import api_bp
from flask import request, session
from ..services.product_service import ProductService
from ..utils.response import success_response, error_response
from ..utils.decorators import login_required
from ..utils.validators import ProductValidator
from ..utils.logger import logger


@api_bp.route('/product/template_types', methods=['GET'])
@login_required
def get_template_types():
    """获取模板类型列表"""
    user_role = session.get('role', 'user')
    template_types = ProductService.get_template_types(user_role)
    return success_response(template_types)


@api_bp.route('/product/products', methods=['GET'])
@login_required
def get_products():
    """根据产线和模板类型获取产品列表"""
    store_code = request.args.get('store_code', '').strip()
    template_type = request.args.get('template_type', '').strip()
    
    logger.info(f"获取产品列表: store_code={store_code}, template_type={template_type}")
    
    if not store_code:
        return error_response('store_code 不能为空')
    
    try:
        products = ProductService.get_products(store_code, template_type)
        logger.info(f"获取到产品列表: {len(products) if isinstance(products, list) else 'N/A'} 条记录")
        return success_response(products)
    except Exception as e:
        logger.error(f"获取产品列表失败: {str(e)}")
        return error_response('获取产品列表失败')


@api_bp.route('/product/product', methods=['GET'])
@login_required
def get_product():
    """获取特定产品的详细信息"""
    sku = request.args.get('sku', '').strip()
    store_code = request.args.get('store_code', '').strip()
    
    if not sku or not store_code:
        return error_response('sku 和 store_code 不能为空')
    
    try:
        product = ProductService.get_product(sku, store_code)
        return success_response(product)
    except Exception as e:
        logger.error(f"获取产品详情失败: {str(e)}")
        return error_response('获取产品详情失败')


@api_bp.route('/product/promo_reason', methods=['GET'])
@login_required
def get_promo_reason():
    """根据SKU获取promo_reason"""
    sku = request.args.get('sku', '').strip()
    store_code = request.args.get('store_code', '').strip()
    
    if not sku or not store_code:
        return error_response('sku 和 store_code 不能为空')
    
    try:
        promo_reason = ProductService.get_promo_reason(sku, store_code)
        return success_response({'promo_reason': promo_reason})
    except Exception as e:
        logger.error(f"获取促销原因失败: {str(e)}")
        return error_response('获取促销原因失败')


@api_bp.route('/product/save', methods=['POST'])
@login_required
def save_product():
    """保存产品信息"""
    data = request.json or {}
    
    # 验证输入
    is_valid, error_msg = ProductValidator.validate_update(data)
    if not is_valid:
        return error_response(error_msg)
    
    sku = data.get('sku')
    store_code = data.get('store_code')
    
    # 移除 sku 和 store_code，其余作为更新字段
    update_data = {k: v for k, v in data.items() if k not in ['sku', 'store_code']}
    
    try:
        success, message = ProductService.save_product(sku, store_code, **update_data)
        if not success:
            return error_response(message)
        return success_response({}, message)
    except Exception as e:
        logger.error(f"保存产品失败: {str(e)}")
        return error_response('保存产品失败')


@api_bp.route('/product/delete', methods=['POST'])
@login_required
def delete_product():
    """删除产品信息"""
    data = request.json or {}
    sku = data.get('sku', '').strip()
    store_code = data.get('store_code', '').strip()
    
    if not sku or not store_code:
        return error_response('sku 和 store_code 不能为空')
    
    try:
        success, message = ProductService.delete_product(sku, store_code)
        if not success:
            return error_response(message)
        return success_response({}, message)
    except Exception as e:
        logger.error(f"删除产品失败: {str(e)}")
        return error_response('删除产品失败')


@api_bp.route('/product/furnace_info', methods=['GET'])
@login_required
def get_furnace_info():
    """获取小循环炉位信息"""
    store_code = request.args.get('store_code', '').strip()
    
    if not store_code:
        return error_response('store_code 不能为空')
    
    try:
        furnace_info = ProductService.get_furnace_info(store_code)
        return success_response(furnace_info)
    except Exception as e:
        logger.error(f"获取炉位信息失败: {str(e)}")
        return error_response('获取炉位信息失败')
