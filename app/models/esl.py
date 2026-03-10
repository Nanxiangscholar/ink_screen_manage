from .base import BaseModel, db
from datetime import datetime


class ESLGoods(BaseModel):
    """电子标签商品绑定模型"""
    __tablename__ = 'hs_esl_goods'
    __bind_key__ = 'storedb'
    
    customer_code = db.Column(db.String(50), nullable=False, index=True)
    store_code = db.Column(db.String(50), nullable=False, index=True)
    esl_id = db.Column(db.String(255), nullable=False, index=True)
    sku = db.Column(db.String(255), nullable=False, index=True)
    position = db.Column(db.Integer, default=0)
    source = db.Column(db.String(50))
    extra = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
    
    __table_args__ = (
        db.Index('idx_esl_sku', 'esl_id', 'sku'),
        db.Index('idx_store_esl', 'store_code', 'esl_id'),
        db.Index('idx_customer_store_sku', 'customer_code', 'store_code', 'sku'),
    )
    
    def to_dict(self):
        """转换为字典"""
        return {
            'customer_code': self.customer_code,
            'store_code': self.store_code,
            'esl_id': self.esl_id,
            'sku': self.sku,
            'position': self.position,
            'source': self.source,
            'extra': self.extra,
            'create_time': self.create_time.isoformat() if self.create_time else None,
        }


class ESL(BaseModel):
    """电子标签模型"""
    __tablename__ = 'hs_esl'
    __bind_key__ = 'storedb'
    
    esl_id = db.Column(db.String(255), nullable=False, unique=True, index=True)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'esl_id': self.esl_id,
        }
