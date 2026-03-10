from ..models.product import Product
from ..models.base import db


# 模板类型到 promo_reason 的映射
TEMPLATE_TYPE_MAPPING = {
    '拉丝': ['21', '22'],
    '成型': ['11', '12'],
    '小循环': ['2'],
    '站台': ['1', '5'],
    '化工': ['3'],
}


class ProductDAO:
    """产品数据访问层"""
    
    @staticmethod
    def get_by_sku(sku, store_code):
        """根据 SKU 和 store_code 获取产品"""
        return Product.query.filter_by(sku=sku, store_code=store_code).first()
    
    @staticmethod
    def get_by_store(store_code, promo_reason=None):
        """根据 store_code 获取产品列表"""
        query = Product.query.filter_by(store_code=store_code)
        if promo_reason:
            query = query.filter_by(promo_reason=promo_reason)
        return query.all()
    
    @staticmethod
    def get_skus_by_store(store_code, template_type=None):
        """根据 store_code 和模板类型获取 SKU 列表"""
        query = Product.query.filter_by(store_code=store_code)
        
        if template_type:
            promo_values = TEMPLATE_TYPE_MAPPING.get(template_type)
            if promo_values:
                query = query.filter(Product.promo_reason.in_(promo_values))
            else:
                # 自定义搜索
                query = query.filter(Product.sku.like(f"%{template_type}%"))
        
        results = query.with_entities(Product.sku).distinct().order_by(Product.sku).all()
        return [item.sku for item in results]
    
    @staticmethod
    def update(product, **kwargs):
        """更新产品信息"""
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        db.session.commit()
        return product
    
    @staticmethod
    def delete(product):
        """删除产品"""
        db.session.delete(product)
        db.session.commit()
    
    @staticmethod
    def get_furnace_info(store_code):
        """获取小循环炉位信息"""
        results = Product.query.filter_by(
            store_code=store_code,
            promo_reason='2'
        ).with_entities(
            Product.sku,
            Product.rsrv_txt1.label('furnace1'),
            Product.rsrv_txt4.label('furnace2'),
            Product.rsrv_txt7.label('furnace3')
        ).all()
        
        return [
            {
                'sku': item.sku,
                'furnace1': item.furnace1,
                'furnace2': item.furnace2,
                'furnace3': item.furnace3
            }
            for item in results
        ]
    
    @staticmethod
    def get_template_types_by_store(store_code):
        """获取门店的模板类型列表"""
        results = Product.query.filter_by(store_code=store_code).with_entities(
            Product.promo_reason
        ).distinct().all()
        
        # 反向映射
        promo_to_type = {
            '21': '拉丝', '22': '拉丝',
            '11': '成型', '12': '成型',
            '2': '小循环',
            '1': '站台', '5': '站台',
            '3': '化工',
        }
        
        types = set()
        for item in results:
            if item.promo_reason:
                type_name = promo_to_type.get(item.promo_reason)
                if type_name:
                    types.add(type_name)
        
        return list(types)
