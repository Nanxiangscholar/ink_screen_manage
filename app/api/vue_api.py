from . import api_bp
from flask import request, jsonify, session
from ..services.product_service import ProductService
from ..services.esl_service import ESLService
from ..services.field_service import FieldService
from ..utils.response import success_response, error_response
from ..utils.decorators import login_required


# Vue 前端 API 路由

@api_bp.route('/products', methods=['GET'])
def vue_get_products():
    """获取产品列表（Vue 前端）"""
    store_code = request.args.get('store_code')
    template_type = request.args.get('template_type')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    
    if not store_code:
        return error_response('产线不能为空')
    
    products = ProductService.get_products(store_code, template_type)
    # 模拟分页
    total = len(products)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_products = products[start:end]
    
    return success_response({
        'items': paginated_products,
        'total': total,
        'page': page,
        'page_size': page_size
    })


@api_bp.route('/products/<int:product_id>', methods=['GET'])
def vue_get_product(product_id):
    """根据ID获取产品详情（Vue 前端）"""
    # 这里需要实现根据ID获取产品的逻辑
    # 暂时返回模拟数据
    product = {
        'id': product_id,
        'sku': 'test_sku',
        'store_code': 'lasiqu',
        'item_name': '测试产品',
        'brand': '测试品牌',
        'unit': '个',
        'promo_reason': '21'
    }
    return success_response(product)


@api_bp.route('/products', methods=['POST'])
def vue_add_product():
    """添加产品（Vue 前端）"""
    data = request.json
    sku = data.get('sku')
    store_code = data.get('store_code')
    
    if not sku or not store_code:
        return error_response('SKU 和产线不能为空')
    
    # 检查产品是否已存在
    existing_product = ProductService.get_product(sku, store_code)
    if existing_product:
        return error_response('产品已存在')
    
    # 这里可以添加更多字段的验证和处理
    # ...
    
    return success_response('产品添加成功')


@api_bp.route('/products/<int:product_id>', methods=['PUT'])
def vue_update_product(product_id):
    """更新产品（Vue 前端）"""
    data = request.json
    sku = data.get('sku')
    store_code = data.get('store_code')
    
    if not sku or not store_code:
        return error_response('SKU 和产线不能为空')
    
    # 移除 sku 和 store_code，其余作为更新字段
    update_data = {k: v for k, v in data.items() if k not in ['sku', 'store_code', 'id']}
    success, message = ProductService.save_product(sku, store_code, **update_data)
    if success:
        return success_response(message)
    else:
        return error_response(message)


@api_bp.route('/products/<int:product_id>', methods=['DELETE'])
def vue_delete_product(product_id):
    """删除产品（Vue 前端）"""
    # 这里需要实现根据ID删除产品的逻辑
    # 暂时返回成功
    return success_response('产品删除成功')


@api_bp.route('/esl', methods=['GET'])
def vue_get_esl_list():
    """获取电子标签列表（Vue 前端）"""
    esl_id = request.args.get('esl_id')
    sku = request.args.get('sku')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    
    # 模拟数据
    esl_list = [
        {
            'id': 1,
            'esl_id': '123456',
            'sku': 'test_sku',
            'store_code': 'lasiqu',
            'position': 5,
            'create_time': '2024-01-01 00:00:00'
        },
        {
            'id': 2,
            'esl_id': '789012',
            'sku': 'test_sku2',
            'store_code': 'chengxing',
            'position': 3,
            'create_time': '2024-01-02 00:00:00'
        }
    ]
    
    # 模拟分页
    total = len(esl_list)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_esl = esl_list[start:end]
    
    return success_response({
        'items': paginated_esl,
        'total': total,
        'page': page,
        'page_size': page_size
    })


@api_bp.route('/esl/bind', methods=['POST'])
def vue_bind_esl():
    """绑定电子标签（Vue 前端）"""
    data = request.json
    esl_id = data.get('esl_id')
    sku = data.get('sku')
    store_code = data.get('store_code')
    position = data.get('position', 5)
    
    if not esl_id or not sku or not store_code:
        return error_response('标签ID、SKU 和产线不能为空')
    
    # 这里可以添加绑定逻辑
    # ...
    
    return success_response('绑定成功')


@api_bp.route('/esl/unbind', methods=['POST'])
def vue_unbind_esl():
    """解绑电子标签（Vue 前端）"""
    data = request.json
    esl_id = data.get('esl_id')
    sku = data.get('sku')
    store_code = data.get('store_code')
    
    if not esl_id or not sku or not store_code:
        return error_response('标签ID、SKU 和产线不能为空')
    
    # 这里可以添加解绑逻辑
    # ...
    
    return success_response('解绑成功')


@api_bp.route('/esl/refresh', methods=['POST'])
def vue_refresh_esl():
    """刷新电子标签（Vue 前端）"""
    data = request.json
    esl_id = data.get('esl_id')
    
    if not esl_id:
        return error_response('标签ID不能为空')
    
    # 这里可以添加刷新逻辑
    # ...
    
    return success_response('刷新成功')


@api_bp.route('/esl/status/<esl_id>', methods=['GET'])
def vue_check_esl_status(esl_id):
    """检查电子标签状态（Vue 前端）"""
    # 这里可以添加检查状态逻辑
    # 暂时返回模拟数据
    status = 'online'
    
    return success_response({'status': status})


@api_bp.route('/fields', methods=['GET'])
def vue_get_fields():
    """获取字段列表（Vue 前端）"""
    field_name = request.args.get('field_name')
    promo_reason = request.args.get('promo_reason')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    
    # 模拟数据
    fields = [
        {
            'id': 1,
            'field_name': 'item_name',
            'label': '产品名称',
            'promo_reason': '21',
            'promo_reason_label': '拉丝'
        },
        {
            'id': 2,
            'field_name': 'brand',
            'label': '品牌',
            'promo_reason': '21',
            'promo_reason_label': '拉丝'
        }
    ]
    
    # 模拟分页
    total = len(fields)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_fields = fields[start:end]
    
    return success_response({
        'items': paginated_fields,
        'total': total,
        'page': page,
        'page_size': page_size
    })


@api_bp.route('/fields', methods=['POST'])
def vue_add_field():
    """添加字段（Vue 前端）"""
    data = request.json
    field_name = data.get('field_name')
    label = data.get('label')
    promo_reason = data.get('promo_reason')
    promo_reason_label = data.get('promo_reason_label')
    
    if not field_name or not label or not promo_reason or not promo_reason_label:
        return error_response('字段名、标签、模板类型和模板类型标签不能为空')
    
    # 这里可以添加添加字段逻辑
    # ...
    
    return success_response('字段添加成功')


@api_bp.route('/fields/<int:field_id>', methods=['PUT'])
def vue_update_field(field_id):
    """更新字段（Vue 前端）"""
    data = request.json
    
    # 这里可以添加更新字段逻辑
    # ...
    
    return success_response('字段更新成功')


@api_bp.route('/fields/<int:field_id>', methods=['DELETE'])
def vue_delete_field(field_id):
    """删除字段（Vue 前端）"""
    # 这里可以添加删除字段逻辑
    # ...
    
    return success_response('字段删除成功')


@api_bp.route('/login', methods=['POST'])
def vue_login():
    """登录（Vue 前端）"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return error_response('用户名和密码不能为空')
    
    # 模拟登录
    if username == 'admin' and password == 'admin':
        # 生成 token
        token = 'test_token_123456'
        return success_response({'token': token, 'username': username})
    else:
        return error_response('用户名或密码错误')
