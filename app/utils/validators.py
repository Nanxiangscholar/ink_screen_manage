"""请求验证工具"""
from typing import Any, Dict, List, Optional, Tuple
from functools import wraps
from flask import request


class ValidationError(Exception):
    """验证错误"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(message)


class Validator:
    """基础验证器"""
    
    @staticmethod
    def required(value: Any, field_name: str) -> Any:
        """验证必填"""
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(f'{field_name}不能为空', field_name)
        return value
    
    @staticmethod
    def string(value: Any, field_name: str, min_len: int = None, max_len: int = None) -> str:
        """验证字符串"""
        if not isinstance(value, str):
            raise ValidationError(f'{field_name}必须是字符串', field_name)
        if min_len and len(value) < min_len:
            raise ValidationError(f'{field_name}长度不能少于{min_len}个字符', field_name)
        if max_len and len(value) > max_len:
            raise ValidationError(f'{field_name}长度不能超过{max_len}个字符', field_name)
        return value
    
    @staticmethod
    def integer(value: Any, field_name: str, min_val: int = None, max_val: int = None) -> int:
        """验证整数"""
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValidationError(f'{field_name}必须是整数', field_name)
        if min_val is not None and value < min_val:
            raise ValidationError(f'{field_name}不能小于{min_val}', field_name)
        if max_val is not None and value > max_val:
            raise ValidationError(f'{field_name}不能大于{max_val}', field_name)
        return value
    
    @staticmethod
    def list_length(value: List, field_name: str, max_items: int = 100) -> List:
        """验证列表长度"""
        if not isinstance(value, list):
            raise ValidationError(f'{field_name}必须是数组', field_name)
        if len(value) > max_items:
            raise ValidationError(f'{field_name}最多包含{max_items}个元素', field_name)
        return value
    
    @staticmethod
    def in_list(value: Any, field_name: str, allowed: List[Any]) -> Any:
        """验证值在允许列表中"""
        if value not in allowed:
            raise ValidationError(f'{field_name}必须是以下值之一: {", ".join(map(str, allowed))}', field_name)
        return value


class ProductValidator(Validator):
    """产品验证器"""
    
    ALLOWED_UPDATE_FIELDS = [
        'item_name', 'unit', 'brand', 'ingredient_table', 'sale_mode',
        'rsrv_txt1', 'rsrv_txt2', 'rsrv_txt3', 'rsrv_txt4', 'rsrv_txt5',
        'rsrv_txt6', 'rsrv_txt7', 'rsrv_txt8', 'rsrv_txt9', 'rsrv_txt10',
        'promo_reason', 'level1_category_name'
    ]
    
    @classmethod
    def validate_update(cls, data: Dict) -> Tuple[bool, Optional[str]]:
        """验证产品更新数据"""
        try:
            cls.required(data.get('sku'), 'SKU')
            cls.required(data.get('store_code'), '门店代码')
            cls.string(data['sku'], 'SKU', min_len=1, max_len=255)
            cls.string(data['store_code'], '门店代码', min_len=1, max_len=50)
            
            # 验证更新字段
            for key, value in data.items():
                if key in ['sku', 'store_code']:
                    continue
                if key not in cls.ALLOWED_UPDATE_FIELDS:
                    raise ValidationError(f'不允许更新字段: {key}', key)
                if isinstance(value, str) and len(value) > 255:
                    raise ValidationError(f'{key}长度不能超过255个字符', key)
            
            return True, None
        except ValidationError as e:
            return False, e.message


class ESLValidator(Validator):
    """ESL 验证器"""
    
    MAX_ESL_IDS = 100
    
    @classmethod
    def validate_esl_ids(cls, esl_ids: List) -> Tuple[bool, Optional[str]]:
        """验证 ESL ID 列表"""
        try:
            cls.required(esl_ids, 'ESL ID列表')
            cls.list_length(esl_ids, 'ESL ID列表', cls.MAX_ESL_IDS)
            return True, None
        except ValidationError as e:
            return False, e.message
    
    @classmethod
    def validate_bind(cls, data: Dict) -> Tuple[bool, Optional[str]]:
        """验证绑定数据"""
        try:
            cls.required(data.get('esl_id'), 'ESL ID')
            cls.required(data.get('sku'), 'SKU')
            cls.string(data['esl_id'], 'ESL ID', min_len=1, max_len=255)
            cls.string(data['sku'], 'SKU', min_len=1, max_len=255)
            return True, None
        except ValidationError as e:
            return False, e.message


class AuthValidator(Validator):
    """认证验证器"""
    
    ALLOWED_ROLES = ['admin', 'user', 'lasiqu_user', 'huagong_user']
    
    @classmethod
    def validate_login(cls, data: Dict) -> Tuple[bool, Optional[str]]:
        """验证登录数据"""
        try:
            cls.required(data.get('username'), '用户名')
            cls.required(data.get('password'), '密码')
            cls.string(data['username'], '用户名', min_len=1, max_len=50)
            cls.string(data['password'], '密码', min_len=1, max_len=100)
            return True, None
        except ValidationError as e:
            return False, e.message
    
    @classmethod
    def validate_register(cls, data: Dict) -> Tuple[bool, Optional[str]]:
        """验证注册数据"""
        try:
            cls.required(data.get('username'), '用户名')
            cls.required(data.get('password'), '密码')
            cls.required(data.get('role'), '角色')
            cls.required(data.get('user_id'), '用户ID')
            cls.required(data.get('invitation_code'), '邀请码')
            
            cls.string(data['username'], '用户名', min_len=3, max_len=20)
            cls.string(data['password'], '密码', min_len=6, max_len=50)
            cls.in_list(data['role'], '角色', cls.ALLOWED_ROLES)
            cls.string(data['user_id'], '用户ID', min_len=1, max_len=50)
            
            return True, None
        except ValidationError as e:
            return False, e.message


def validate_request(validator_class, method_name: str):
    """请求验证装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.json or {}
            validator = getattr(validator_class, method_name)
            is_valid, error_msg = validator(data)
            
            if not is_valid:
                from .response import error_response
                return error_response(error_msg)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
