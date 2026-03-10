"""应用配置管理"""
import os
from typing import Optional


class Config:
    """基础配置"""
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:root@20.203.201.251:3307/goods'
    )
    SQLALCHEMY_BINDS: dict = {
        'storedb': os.getenv(
            'DATABASE_URL_STOREDB',
            'mysql+pymysql://root:root@20.203.201.251:3307/storedb'
        ),
        'eslworking': os.getenv(
            'DATABASE_URL_ESLWORKING',
            'mysql+pymysql://root:root@20.203.201.251:3307/eslworking'
        )
    }
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    # Session 安全配置
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = 'Lax'
    SESSION_COOKIE_SECURE: bool = os.getenv('SESSION_COOKIE_SECURE', 'false').lower() == 'true'
    
    # 外部服务配置
    PRISMART_BASE_URL: str = os.getenv('PRISMART_BASE_URL', 'http://20.203.201.251:8090')
    PRISMART_USERNAME: str = os.getenv('PRISMART_USERNAME', 'hs-admin')
    PRISMART_PASSWORD: str = os.getenv('PRISMART_PASSWORD', '000000')
    PRISMART_CUSTOMER_CODE: str = os.getenv('PRISMART_CUSTOMER_CODE', 'hs')
    PRISMART_STORE_CODE: str = os.getenv('PRISMART_STORE_CODE', '101')
    
    # 应用配置
    INVITATION_CODE: str = os.getenv('INVITATION_CODE', 'jushi')
    
    @classmethod
    def validate(cls) -> list:
        """验证必要的配置项，返回缺失的配置列表"""
        missing = []
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            missing.append('SECRET_KEY')
        return missing


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG: bool = True
    SESSION_COOKIE_SECURE: bool = False


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG: bool = False
    SESSION_COOKIE_SECURE: bool = True
    
    @classmethod
    def validate(cls) -> list:
        missing = super().validate()
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            missing.append('SECRET_KEY (必须设置生产密钥)')
        if cls.PRISMART_PASSWORD == '000000':
            missing.append('PRISMART_PASSWORD (生产环境必须更改)')
        return missing


class TestingConfig(Config):
    """测试环境配置"""
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///:memory:'


# 配置映射
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}


def get_config() -> Config:
    """根据环境获取配置"""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
