from ..dao.product_dao import ProductDAO
from ..models.product import Product
from ..models.base import db
from ..utils.cache import cache, cache_manager
from datetime import timedelta


class ProductService:
    """产品服务"""
    
    @staticmethod
    @cache("template_types:{0}", expire=timedelta(hours=1))
    def get_template_types(user_role):
        """获取模板类型列表"""
        all_template_types = {
            '拉丝': '拉丝',
            '成型': '成型',
            '站台': '站台',
            '化工': '化工'
        }
        
        if user_role == 'lasiquuser':
            # lasiquuser 不显示化工选项
            template_types = {k: v for k, v in all_template_types.items() if k != '化工'}
        else:
            template_types = all_template_types
        
        return template_types
    
    @staticmethod
    @cache("products:{0}:{1}", expire=timedelta(minutes=30))
    def get_products(store_code, template_type=None):
        """根据产线和模板类型获取产品列表"""
        return ProductDAO.get_skus_by_store(store_code, template_type)
    
    @staticmethod
    @cache("product:{0}:{1}", expire=timedelta(minutes=15))
    def get_product(sku, store_code):
        """获取特定产品的详细信息"""
        product = ProductDAO.get_by_sku(sku, store_code)
        if not product:
            return {}
        
        # 转换为字典
        result = {
            'id': product.id,
            'sku': product.sku,
            'store_code': product.store_code,
            'item_name': product.item_name,
            'unit': product.unit,
            'brand': product.brand,
            'ingredient_table': product.ingredient_table,
            'sale_mode': product.sale_mode,
            'rsrv_txt1': product.rsrv_txt1,
            'rsrv_txt2': product.rsrv_txt2,
            'rsrv_txt3': product.rsrv_txt3,
            'rsrv_txt4': product.rsrv_txt4,
            'rsrv_txt5': product.rsrv_txt5,
            'rsrv_txt6': product.rsrv_txt6,
            'rsrv_txt7': product.rsrv_txt7,
            'rsrv_txt8': product.rsrv_txt8,
            'rsrv_txt9': product.rsrv_txt9,
            'rsrv_txt10': product.rsrv_txt10,
            'promo_reason': product.promo_reason,
            'level1_category_name': product.level1_category_name,
            'create_time': product.create_time.isoformat() if product.create_time else None,
            'update_time': product.update_time.isoformat() if product.update_time else None
        }
        
        # 处理 ingredient_table 字段，确保它是完整的 data URI
        if result.get('ingredient_table'):
            image_data = result['ingredient_table']
            # 检查是否已经是完整的 data URI
            if not image_data.startswith('data:image/'):
                # 检查图片格式并添加相应前缀
                if image_data.startswith('/9j/'):
                    result['ingredient_table'] = f'data:image/jpeg;base64,{image_data}'
                elif image_data.startswith('iVBORw0KGgo'):
                    result['ingredient_table'] = f'data:image/png;base64,{image_data}'
                else:
                    # 默认使用JPEG格式
                    result['ingredient_table'] = f'data:image/jpeg;base64,{image_data}'
        
        return result
    
    @staticmethod
    @cache("promo_reason:{0}:{1}", expire=timedelta(minutes=30))
    def get_promo_reason(sku, store_code):
        """根据SKU获取promo_reason"""
        product = ProductDAO.get_by_sku(sku, store_code)
        return product.promo_reason if product else None
    
    @staticmethod
    def save_product(sku, store_code, **kwargs):
        """保存产品信息"""
        try:
            product = ProductDAO.get_by_sku(sku, store_code)
            if not product:
                return False, '产品不存在'
            
            # 定义所有可能的字段
            all_fields = [
                'item_name', 'unit', 'brand', 'ingredient_table', 'sale_mode',
                'rsrv_txt1', 'rsrv_txt2', 'rsrv_txt3', 'rsrv_txt4', 'rsrv_txt5',
                'rsrv_txt6', 'rsrv_txt7', 'rsrv_txt8', 'rsrv_txt9', 'rsrv_txt10',
                'promo_reason', 'level1_category_name'
            ]
            
            # 只处理实际传入的字段
            update_data = {}
            for field in all_fields:
                if field in kwargs:
                    value = kwargs.get(field, '')
                    # 特别处理 ingredient_table 字段，确保存储的是纯base64数据
                    if field == 'ingredient_table' and isinstance(value, str):
                        # 如果是完整的 data URI，只保存 base64 部分
                        if value.startswith('data:image/'):
                            base64_data = value.split(',')[1] if ',' in value else value
                            update_data[field] = base64_data
                        else:
                            update_data[field] = value
                    else:
                        update_data[field] = value
            
            if not update_data:
                return False, '没有有效的字段需要更新'
            
            # 更新产品信息
            ProductDAO.update(product, **update_data)
            
            # 清除缓存
            cache_manager.clear_pattern(f"product:{sku}:{store_code}")
            cache_manager.clear_pattern(f"products:{store_code}:*")
            cache_manager.clear_pattern(f"promo_reason:{sku}:{store_code}")
            
            return True, '产品信息更新成功'
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def delete_product(sku, store_code):
        """删除产品信息"""
        try:
            product = ProductDAO.get_by_sku(sku, store_code)
            if not product:
                return False, '产品不存在'
            
            ProductDAO.delete(product)
            
            # 清除缓存
            cache_manager.clear_pattern(f"product:{sku}:{store_code}")
            cache_manager.clear_pattern(f"products:{store_code}:*")
            cache_manager.clear_pattern(f"promo_reason:{sku}:{store_code}")
            
            return True, '产品信息删除成功'
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    @cache("furnace_info:{0}", expire=timedelta(minutes=10))
    def get_furnace_info(store_code):
        """获取小循环炉位信息"""
        return ProductDAO.get_furnace_info(store_code)
