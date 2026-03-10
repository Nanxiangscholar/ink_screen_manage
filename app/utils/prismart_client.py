import requests
import hashlib
import os
from typing import Optional, Dict, Any, List
import concurrent.futures
from threading import Lock

from .logger import logger

class PrismartClient:
    """Prismart 电子标签系统 API 客户端"""

    def __init__(self, base_url: str = None):
        # 从环境变量获取基础URL，如果没有则使用默认值
        self.base_url = base_url or os.getenv(
            'PRISMART_API_URL',
            'http://20.203.201.251:8090/prismart/openapi3'
        )
        self.session = requests.Session()
        # 设置超时时间
        self.timeout = int(os.getenv('PRISMART_TIMEOUT', '30'))
        self.logged_in = False
        self.username = None
        self.jsessionid = None

    def login(self, username: str, password: str) -> bool:
        """
        登录并获取 jsessionid
        """
        self.username = username

        # 从环境变量获取密码，如果参数为空的话
        if not password:
            password = os.getenv('PRISMART_PASSWORD', '')

        # 构造加密后的密码：MD5(password + username)
        auth_string = password + username
        authentication = hashlib.md5(auth_string.encode('utf-8')).hexdigest()

        data = {
            'username': username,
            'authentication': authentication
        }

        login_url = f"{self.base_url}/account/login/authentication"

        try:
            response = self.session.post(
                login_url,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()

            if result.get('code') == 1001 and result.get('result') == 'succeed':
                self.logged_in = True
                self.jsessionid = result['data']['jsessionid']
                logger.info(f"登录成功！jsessionid: {self.jsessionid}")
                return True
            else:
                logger.error(f"登录失败: {result}")
                return False
        except requests.exceptions.Timeout:
            logger.error(f"登录超时: 请求超过 {self.timeout} 秒")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"登录网络异常: {e}")
            return False
        except Exception as e:
            logger.error(f"登录异常: {e}")
            return False

    def _auto_retry_login(self) -> bool:
        """
        自动重试登录
        """
        if self.username:
            # 从环境变量获取密码
            password = os.getenv('PRISMART_PASSWORD', '')
            if password:
                logger.info("🔄 尝试自动重新登录...")
                return self.login(self.username, password)

        logger.error("❌ 无登录凭据，无法自动登录")
        return False

    def _make_request_with_retry(self, method: str, url: str, **kwargs) -> Optional[Dict[Any, Any]]:
        """
        带重试机制的请求包装器
        """
        # 设置默认超时时间
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error(f"❌ 请求超时: {url}")
            return None
        except Exception as e:
            # 检查是否是认证相关的错误
            if "401" in str(e) or "403" in str(e):
                logger.info("🔐 检测到认证失败，尝试重新登录...")
                if self._auto_retry_login():
                    # 重新登录成功，再次尝试请求
                    try:
                        # 更新headers中的jsessionid
                        if self.jsessionid and 'headers' in kwargs:
                            kwargs['headers']['Cookie'] = f"JSESSIONID={self.jsessionid}"

                        response = self.session.request(method, url, **kwargs)
                        response.raise_for_status()
                        return response.json()
                    except Exception as retry_e:
                        logger.error(f"❌ 重试请求失败: {retry_e}")
                        return None
                else:
                    logger.error("❌ 自动登录失败")
                    return None
            else:
                raise e

    def get_label_last_refresh_status(self, label_id: str, customer_code: str, store_code: str) -> Optional[int]:
        """
        获取标签的 lastRefreshStatus 状态
        """
        if not self.logged_in:
            logger.error("❌ 未登录，请先调用 login()")
            return None

        url = (
            f"{self.base_url}/store/labels/detail/{label_id}"
            f"?customer-code={customer_code}&store-code={store_code}"
        )
        result = self._make_request_with_retry('GET', url)

        # 提取 lastRefreshStatus 字段
        if result and 'data' in result and 'lastRefreshStatus' in result['data']:
            status = result['data']['lastRefreshStatus']
            return status
        else:
            logger.error("❌ 未找到 lastRefreshStatus 字段")
            return None

    def get_label_detail(self, label_id: str, customer_code: str, store_code: str) -> Optional[Dict[Any, Any]]:
        """
        获取标签详情
        """
        if not self.logged_in:
            logger.error("❌ 未登录，请先调用 login()")
            return None

        url = (
            f"{self.base_url}/store/labels/detail/{label_id}"
            f"?customer-code={customer_code}&store-code={store_code}"
        )
        return self._make_request_with_retry('GET', url)

    def bind_label(self, customer_code: str, store_code: str, label_id: str, sku: str, position: int = 5) -> Optional[Dict[Any, Any]]:
        """
        绑定标签到商品 (使用 PUT 方法)
        """
        if not self.logged_in:
            logger.error("❌ 未登录，请先调用 login()")
            return None

        url = (
            f"{self.base_url}/store/links"
            f"?customer-code={customer_code}&store-code={store_code}"
        )
        data = [{
            "labelId": label_id,
            "position": position,
            "sku": sku
        }]

        return self._make_request_with_retry('PUT', url, json=data)

    def unbind_label(self, customer_code: str, store_code: str, label_id: str, sku: str, position: int = 5) -> Optional[Dict[Any, Any]]:
        """
        解绑标签 (使用 DELETE 方法)
        """
        if not self.logged_in:
            logger.error("❌ 未登录，请先调用 login()")
            return None

        url = (
            f"{self.base_url}/store/links"
            f"?customer-code={customer_code}&store-code={store_code}"
        )
        data = [{
            "labelId": label_id,
            "position": position,
            "sku": sku
        }]

        return self._make_request_with_retry('DELETE', url, json=data)

    def batch_get_label_status(self, label_ids: List[str], customer_code: str, store_code: str) -> Dict[str, str]:
        """
        批量获取标签状态

        Args:
            label_ids: 标签ID列表
            customer_code: 客户代码
            store_code: 门店代码

        Returns:
            Dict[str, str]: 标签字典，键为标签ID，值为状态(online/offline/unknown)
        """
        status_dict = {}

        # 创建锁保护共享资源
        lock = Lock()

        def get_single_status(esl_id):
            try:
                # 获取标签详细信息
                status = self.get_label_last_refresh_status(
                    label_id=esl_id,
                    customer_code=customer_code,
                    store_code=store_code
                )

                # 根据 lastRefreshStatus 判断状态
                # 0 为正常，其他为异常
                status_text = 'online' if status == 0 else 'offline' if status is not None else 'unknown'

                # 线程安全地更新字典
                with lock:
                    status_dict[esl_id] = status_text

            except Exception as e:
                logger.error(f"获取标签 {esl_id} 状态失败: {str(e)}")
                with lock:
                    status_dict[esl_id] = 'unknown'

        # 控制并发数，避免连接池满的问题
        max_workers = min(10, len(label_ids), 20)  # 最大不超过20个线程

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_esl = {executor.submit(get_single_status, esl_id): esl_id for esl_id in label_ids}

            # 等待所有任务完成
            for future in concurrent.futures.as_completed(future_to_esl):
                try:
                    future.result()  # 获取结果，即使不需要也可以触发异常处理
                except Exception as e:
                    esl_id = future_to_esl[future]
                    logger.error(f"处理标签 {esl_id} 时发生异常: {str(e)}")
                    with lock:
                        status_dict[esl_id] = 'unknown'

        return status_dict
