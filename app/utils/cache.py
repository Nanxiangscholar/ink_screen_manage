import json
import time
from datetime import timedelta

class LocalCache:
    """本地内存缓存"""
    def __init__(self):
        self.cache = {}
    
    def get(self, key):
        """获取缓存"""
        if key in self.cache:
            value, expire_time = self.cache[key]
            if expire_time is None or time.time() < expire_time:
                return value
            else:
                # 缓存已过期
                del self.cache[key]
        return None
    
    def set(self, key, value, expire=None):
        """设置缓存"""
        if expire:
            expire_time = time.time() + expire
        else:
            expire_time = None
        self.cache[key] = (value, expire_time)
        return True
    
    def delete(self, key):
        """删除缓存"""
        if key in self.cache:
            del self.cache[key]
        return True
    
    def clear_pattern(self, pattern):
        """清除匹配模式的缓存"""
        # 简单实现，仅删除完全匹配的键
        if pattern in self.cache:
            del self.cache[pattern]
        return True

class CacheManager:
    """缓存管理器"""

    def __init__(self, host='localhost', port=6379, db=0):
        # 直接使用本地缓存，避免 Redis 连接问题
        print("使用本地缓存")
        self.available = False
        self.local_cache = LocalCache()

    def get(self, key):
        """获取缓存"""
        return self.local_cache.get(key)

    def set(self, key, value, expire=None):
        """设置缓存"""
        return self.local_cache.set(key, value, expire)

    def delete(self, key):
        """删除缓存"""
        return self.local_cache.delete(key)

    def clear_pattern(self, pattern):
        """清除匹配模式的缓存"""
        return self.local_cache.clear_pattern(pattern)

# 全局缓存管理器实例
cache_manager = CacheManager()

def cache(key_pattern, expire=timedelta(minutes=10)):
    """缓存装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 生成缓存键
            key = key_pattern
            for i, arg in enumerate(args):
                key = key.replace(f"{{{i}}}", str(arg))
            for k, v in kwargs.items():
                key = key.replace(f"{{{k}}}", str(v))

            # 尝试从缓存获取
            cached_value = cache_manager.get(key)
            if cached_value is not None:
                return cached_value

            # 执行函数
            result = func(*args, **kwargs)

            # 缓存结果
            cache_manager.set(key, result, expire.total_seconds())

            return result
        return wrapper
    return decorator
