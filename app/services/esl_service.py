from ..dao.esl_dao import ESLDAO
from ..utils.prismart_client import PrismartClient
from ..config import get_config
from ..utils.logger import logger


class ESLService:
    """电子标签服务"""
    
    def __init__(self):
        self.client = PrismartClient()
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        config = get_config()
        self.prismart_username = config.PRISMART_USERNAME
        self.prismart_password = config.PRISMART_PASSWORD
        self.customer_code = config.PRISMART_CUSTOMER_CODE
        self.store_code = config.PRISMART_STORE_CODE
    
    def _ensure_logged_in(self):
        """确保已登录"""
        if not self.client.logged_in:
            if not self.client.login(self.prismart_username, self.prismart_password):
                logger.error("Prismart 登录失败")
                return False
        return True
    
    def get_esl_goods(self, sku=None, esl_id=None):
        """获取电子标签商品绑定信息"""
        return ESLDAO.get_esl_goods(sku, esl_id)
    
    def _handle_api_response(self, result, action_name: str) -> tuple:
        """统一处理 API 响应"""
        if not result:
            logger.error(f"{action_name}失败: API 返回为空")
            return False, f'{action_name}失败: API 返回为空'
        
        if result.get('code') != 1001:
            error_msg = result.get('msg', '未知错误')
            logger.error(f"{action_name}失败: {error_msg}")
            return False, f'{action_name}失败: {error_msg}'
        
        logger.info(f"{action_name}成功")
        return True, f'{action_name}成功'
    
    def bind_label(self, esl_id, sku):
        """绑定标签到商品"""
        if not self._ensure_logged_in():
            return False, '登录失败，无法绑定'
        
        result = self.client.bind_label(
            customer_code=self.customer_code,
            store_code=self.store_code,
            label_id=esl_id,
            sku=sku,
            position=0
        )
        
        return self._handle_api_response(result, '绑定')
    
    def unbind_label(self, esl_id, sku):
        """解绑标签"""
        if not self._ensure_logged_in():
            return False, '登录失败，无法解绑'
        
        result = self.client.unbind_label(
            customer_code=self.customer_code,
            store_code=self.store_code,
            label_id=esl_id,
            sku=sku,
            position=0
        )
        
        return self._handle_api_response(result, '解绑')
    
    def get_esl_ids(self):
        """获取所有电子标签 ID"""
        return ESLDAO.get_esl_ids()
    
    def get_skus(self, role):
        """根据角色获取 SKU 列表"""
        return ESLDAO.get_skus_by_role(role)
    
    def get_esl_status(self, esl_ids):
        """批量获取标签状态"""
        if not self._ensure_logged_in():
            return []
        
        return self.client.batch_get_label_status(
            label_ids=esl_ids,
            customer_code=self.customer_code,
            store_code=self.store_code
        )


# 延迟初始化的电子标签服务实例
_esl_service = None


def get_esl_service():
    """获取电子标签服务实例（延迟初始化）"""
    global _esl_service
    if _esl_service is None:
        _esl_service = ESLService()
    return _esl_service


# 保持向后兼容
esl_service = property(lambda self: get_esl_service())
