from ..dao.field_dao import FieldDAO
from ..models.product import Product
from ..models.field import FieldLabel
from ..models.base import db


class FieldService:
    """字段标签服务"""
    
    @staticmethod
    def get_table_fields():
        """获取finall表的所有字段信息和标签映射"""
        try:
            # 获取表结构信息（使用 SQLAlchemy 的 inspect）
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = inspector.get_columns('finall')
            
            # 确保field_labels表存在（由 SQLAlchemy 自动创建）
            db.create_all()
            
            # 获取字段标签映射
            label_mappings = {}
            field_labels = FieldLabel.query.filter_by(promo_reason=None).all()
            for field_label in field_labels:
                label_mappings[field_label.field_name] = field_label.label
            
            # 转换为字段列表
            fields = []
            for column in columns:
                field_name = column['name']
                field_type = str(column['type'])
                field_null = 'YES' if column['nullable'] else 'NO'
                field_key = 'PRI' if column.get('primary_key') else ''
                field_default = column.get('default', None)
                field_extra = ''
                
                label = label_mappings.get(field_name, field_name)
                field_info = {
                    'field': field_name,
                    'type': field_type,
                    'null': field_null,
                    'key': field_key,
                    'default': field_default,
                    'extra': field_extra,
                    'label': label
                }
                fields.append(field_info)
            
            return fields, label_mappings
        except Exception as e:
            print(f"获取表字段信息失败: {str(e)}")
            return [], {}
    
    @staticmethod
    def update_field_label(field_name, label):
        """更新字段标签"""
        try:
            FieldDAO.create_or_update_field_label(field_name, label)
            return True, f'字段 {field_name} 的标签已更新为 {label}'
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_template_fields(promo_reason):
        """获取模板字段映射"""
        return FieldDAO.get_template_fields(promo_reason)
    
    @staticmethod
    def update_template_field(field_name, label, promo_reason, promo_reason_label=None):
        """更新模板字段映射"""
        try:
            FieldDAO.create_or_update_field_label(
                field_name, label, promo_reason, promo_reason_label
            )
            return True, f'模板 {promo_reason} 的字段 {field_name} 标签已更新为 {label}'
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def delete_template_field(field_name, promo_reason):
        """删除模板字段映射"""
        try:
            success = FieldDAO.delete_field_label(field_name, promo_reason)
            if success:
                return True, f'模板 {promo_reason} 的字段 {field_name} 已删除'
            else:
                return False, '字段标签不存在'
        except Exception as e:
            return False, str(e)
