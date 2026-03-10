from .base import BaseModel, db


class Product(BaseModel):
    """产品模型"""
    __tablename__ = 'finall'
    
    sku = db.Column(db.String(255), nullable=False, index=True)
    store_code = db.Column(db.String(50), nullable=False, index=True)
    item_name = db.Column(db.String(255))
    unit = db.Column(db.String(50))
    brand = db.Column(db.String(255))
    ingredient_table = db.Column(db.Text)
    sale_mode = db.Column(db.String(50))
    rsrv_txt1 = db.Column(db.String(255))  # 预留字段1
    rsrv_txt2 = db.Column(db.String(255))  # 预留字段2
    rsrv_txt3 = db.Column(db.String(255))  # 预留字段3
    rsrv_txt4 = db.Column(db.String(255))  # 预留字段4
    rsrv_txt5 = db.Column(db.String(255))  # 预留字段5
    rsrv_txt6 = db.Column(db.String(255))  # 预留字段6
    rsrv_txt7 = db.Column(db.String(255))  # 预留字段7
    rsrv_txt8 = db.Column(db.String(255))  # 预留字段8
    rsrv_txt9 = db.Column(db.String(255))  # 预留字段9
    rsrv_txt10 = db.Column(db.String(255))  # 预留字段10
    promo_reason = db.Column(db.String(50), index=True)  # 模板类型
    level1_category_name = db.Column(db.String(255))  # 分类名称
    
    __table_args__ = (
        db.Index('idx_sku_store', 'sku', 'store_code'),
        db.Index('idx_store_promo', 'store_code', 'promo_reason'),
        db.Index('idx_promo_reason', 'promo_reason'),
    )
    
    def to_dict(self):
        """转换为字典"""
        return {
            'sku': self.sku,
            'store_code': self.store_code,
            'item_name': self.item_name,
            'unit': self.unit,
            'brand': self.brand,
            'ingredient_table': self.ingredient_table,
            'sale_mode': self.sale_mode,
            'promo_reason': self.promo_reason,
            'level1_category_name': self.level1_category_name,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'update_time': self.update_time.isoformat() if self.update_time else None,
        }
