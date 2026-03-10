from ..models.esl import ESLGoods, ESL
from ..models.product import Product
from ..models.base import db


# 角色到产品类型的映射
ROLE_PROMO_MAPPING = {
    'lasiqu_user': [1, 11, 12, 21, 22, 5],
    'huagong_user': [3],
    'admin': [1, 2, 3, 11, 12, 21, 22, 111, 5],
    'user': [1, 2, 3, 11, 12, 21, 22, 111, 5],
}

# 旧角色名称兼容（修复拼写错误）
LEGACY_ROLE_MAPPING = {
    'lasiquuser': 'lasiqu_user',
    'huagonguuser': 'huagong_user',
}


class ESLDAO:
    """电子标签数据访问层"""
    
    @staticmethod
    def get_esl_goods(sku=None, esl_id=None):
        """获取电子标签商品绑定信息"""
        query = ESLGoods.query
        
        if sku:
            query = query.filter_by(sku=sku)
        if esl_id:
            query = query.filter_by(esl_id=esl_id)
        
        results = query.with_entities(
            ESLGoods.customer_code,
            ESLGoods.store_code,
            ESLGoods.esl_id,
            ESLGoods.sku,
            ESLGoods.position,
            ESLGoods.source,
            ESLGoods.extra,
            ESLGoods.create_time
        ).order_by(ESLGoods.create_time.desc()).all()
        
        return [
            {
                'customer_code': item.customer_code,
                'store_code': item.store_code,
                'esl_id': item.esl_id,
                'sku': item.sku,
                'position': item.position,
                'source': item.source,
                'extra': item.extra,
                'create_time': item.create_time.isoformat() if item.create_time else None
            }
            for item in results
        ]
    
    @staticmethod
    def get_esl_ids():
        """获取所有电子标签 ID"""
        results = ESL.query.with_entities(ESL.esl_id).all()
        return [item.esl_id for item in results]
    
    @staticmethod
    def get_skus_by_role(role):
        """根据角色获取 SKU 列表"""
        # 兼容旧的角色名称
        normalized_role = LEGACY_ROLE_MAPPING.get(role, role)
        
        promo_values = ROLE_PROMO_MAPPING.get(normalized_role, ROLE_PROMO_MAPPING['user'])
        
        results = Product.query.filter(
            Product.promo_reason.in_(promo_values)
        ).with_entities(Product.sku).distinct().all()
        
        return [item.sku for item in results]
    
    @staticmethod
    def get_by_esl_id(esl_id):
        """根据 ESL ID 获取绑定信息"""
        return ESLGoods.query.filter_by(esl_id=esl_id).first()
    
    @staticmethod
    def get_by_sku(sku):
        """根据 SKU 获取绑定信息列表"""
        return ESLGoods.query.filter_by(sku=sku).all()
