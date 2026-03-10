import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime


class Logger:
    """日志管理器"""
    
    _instances = {}
    
    def __new__(cls, name=__name__):
        """单例模式，每个名称一个实例"""
        if name not in cls._instances:
            cls._instances[name] = super().__new__(cls)
            cls._instances[name]._initialized = False
        return cls._instances[name]
    
    def __init__(self, name=__name__):
        if self._initialized:
            return
        self._initialized = True
        
        # 创建日志目录
        log_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            'logs'
        )
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建日志文件路径
        log_file = os.path.join(log_dir, 'app.log')
        
        # 创建 logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        console_handler.encoding = 'utf-8'
        
        # 创建文件处理器
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # 添加处理器（避免重复添加）
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def debug(self, message, **kwargs):
        """记录调试信息"""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def info(self, message, **kwargs):
        """记录信息"""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message, **kwargs):
        """记录警告"""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message, exc_info=False, **kwargs):
        """记录错误"""
        self.logger.error(self._format_message(message, **kwargs), exc_info=exc_info)
    
    def critical(self, message, exc_info=False, **kwargs):
        """记录严重错误"""
        self.logger.critical(self._format_message(message, **kwargs), exc_info=exc_info)
    
    @staticmethod
    def _format_message(message, **kwargs):
        """格式化消息"""
        if kwargs:
            extra = ' | '.join(f'{k}={v}' for k, v in kwargs.items())
            return f'{message} | {extra}'
        return message


# 全局日志实例
logger = Logger('app')


def get_logger(name: str) -> Logger:
    """获取指定名称的日志实例"""
    return Logger(name)
