from flask import Flask
from flask_cors import CORS
from .models.base import db
from .utils.exceptions import register_error_handlers
from .config import get_config


def create_app(config_name=None):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 加载配置
    if config_name:
        from .config import config_by_name
        config = config_by_name.get(config_name)
    else:
        config = get_config()
    
    app.config.from_object(config)
    
    # 验证配置
    missing_configs = config.validate()
    if missing_configs and config.DEBUG:
        print(f"[WARNING] 缺少配置项: {', '.join(missing_configs)}")
    
    # 初始化插件
    db.init_app(app)
    CORS(app, supports_credentials=True)
    
    # 注册错误处理器
    register_error_handlers(app)
    
    # 导入并注册蓝图
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from .routes import routes_bp
    app.register_blueprint(routes_bp)
    
    return app
