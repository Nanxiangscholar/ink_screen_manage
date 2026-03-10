from . import api_bp
from flask import request, jsonify, session
from ..services.field_service import FieldService
from ..utils.response import success_response, error_response
from ..utils.decorators import login_required


@api_bp.route('/field/table_fields', methods=['GET'])
@login_required
def get_table_fields():
    """获取finall表的所有字段信息和标签映射"""
    fields, label_mappings = FieldService.get_table_fields()
    return success_response({'fields': fields, 'label_mappings': label_mappings})


@api_bp.route('/field/update_label', methods=['POST'])
@login_required
def update_field_label():
    """更新字段标签"""
    data = request.json
    field_name = data.get('field_name')
    label = data.get('label')
    
    if not field_name or not label:
        return error_response('field_name and label are required')
    
    success, message = FieldService.update_field_label(field_name, label)
    
    if not success:
        return error_response(message)
    
    return success_response({}, message)


@api_bp.route('/field/template_fields', methods=['GET'])
@login_required
def get_template_fields():
    """获取模板字段映射"""
    promo_reason = request.args.get('promo_reason')
    
    if not promo_reason:
        return error_response('promo_reason is required')
    
    fields = FieldService.get_template_fields(promo_reason)
    return success_response(fields)


@api_bp.route('/field/update_template_field', methods=['POST'])
@login_required
def update_template_field():
    """更新模板字段映射"""
    data = request.json
    field_name = data.get('field_name')
    label = data.get('label')
    promo_reason = data.get('promo_reason')
    promo_reason_label = data.get('promo_reason_label')
    
    if not field_name or not label or not promo_reason:
        return error_response('field_name, label and promo_reason are required')
    
    success, message = FieldService.update_template_field(
        field_name, label, promo_reason, promo_reason_label
    )
    
    if not success:
        return error_response(message)
    
    return success_response({}, message)


@api_bp.route('/field/delete_template_field', methods=['POST'])
@login_required
def delete_template_field():
    """删除模板字段映射"""
    data = request.json
    field_name = data.get('field_name')
    promo_reason = data.get('promo_reason')
    
    if not field_name or not promo_reason:
        return error_response('field_name and promo_reason are required')
    
    success, message = FieldService.delete_template_field(field_name, promo_reason)
    
    if not success:
        return error_response(message)
    
    return success_response({}, message)
