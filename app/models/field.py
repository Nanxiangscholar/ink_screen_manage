from .base import BaseModel, db


class FieldLabel(BaseModel):
    """字段标签模型"""
    __tablename__ = 'field_labels'
    
    field_name = db.Column(db.String(255), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    promo_reason = db.Column(db.String(255), nullable=True)
    promo_reason_label = db.Column(db.String(255), nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint('field_name', 'promo_reason', name='unique_field_promo'),
    )
