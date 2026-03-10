from ..models.field import FieldLabel
from ..models.base import db


class FieldDAO:
    """字段标签数据访问层"""
    
    @staticmethod
    def get_field_labels():
        """获取所有字段标签映射"""
        return FieldLabel.query.with_entities(
            FieldLabel.field_name,
            FieldLabel.label,
            FieldLabel.promo_reason,
            FieldLabel.promo_reason_label
        ).all()
    
    @staticmethod
    def get_field_label(field_name, promo_reason=None):
        """根据字段名和模板类型获取标签"""
        return FieldLabel.query.filter_by(
            field_name=field_name,
            promo_reason=promo_reason
        ).first()
    
    @staticmethod
    def get_template_fields(promo_reason):
        """获取指定模板的字段映射"""
        results = FieldLabel.query.with_entities(
            FieldLabel.field_name,
            FieldLabel.label
        ).filter_by(
            promo_reason=promo_reason.strip()
        ).order_by(FieldLabel.field_name).all()
        
        template_fields = {}
        for item in results:
            template_fields[item.field_name] = item.label
        return template_fields
    
    @staticmethod
    def create_or_update_field_label(field_name, label, promo_reason=None, promo_reason_label=None):
        """创建或更新字段标签"""
        field_label = FieldDAO.get_field_label(field_name, promo_reason)
        if field_label:
            field_label.label = label
            if promo_reason_label:
                field_label.promo_reason_label = promo_reason_label
        else:
            field_label = FieldLabel(
                field_name=field_name,
                label=label,
                promo_reason=promo_reason,
                promo_reason_label=promo_reason_label
            )
            db.session.add(field_label)
        db.session.commit()
        return field_label
    
    @staticmethod
    def delete_field_label(field_name, promo_reason):
        """删除字段标签"""
        field_label = FieldDAO.get_field_label(field_name, promo_reason)
        if field_label:
            db.session.delete(field_label)
            db.session.commit()
            return True
        return False
