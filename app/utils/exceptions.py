"""异常处理模块"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
import traceback
from .logger import logger


class AppException(Exception):
    """应用异常基类"""
    
    def __init__(self, message: str, code: int = 400, details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)


class ValidationError(AppException):
    """验证错误"""
    
    def __init__(self, message: str, field: str = None):
        details = {'field': field} if field else {}
        super().__init__(message, code=400, details=details)


class AuthenticationError(AppException):
    """认证错误"""
    
    def __init__(self, message: str = '认证失败'):
        super().__init__(message, code=401)


class PermissionError(AppException):
    """权限错误"""
    
    def __init__(self, message: str = '权限不足'):
        super().__init__(message, code=403)


class NotFoundError(AppException):
    """资源未找到"""
    
    def __init__(self, message: str = '资源未找到'):
        super().__init__(message, code=404)


class DatabaseError(AppException):
    """数据库错误"""
    
    def __init__(self, message: str = '数据库操作失败'):
        super().__init__(message, code=500)


def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(AppException)
    def handle_app_exception(e):
        """处理应用异常"""
        logger.warning(f"应用异常: {e.message}", code=e.code)
        return jsonify({
            'success': False,
            'data': e.details,
            'message': e.message
        }), e.code
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """处理HTTP异常"""
        logger.warning(f"HTTP异常: {e.description}", code=e.code)
        return jsonify({
            'success': False,
            'data': None,
            'message': e.description or '请求错误'
        }), e.code or 400
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        """处理错误请求"""
        return jsonify({
            'success': False,
            'data': None,
            'message': '请求参数错误'
        }), 400
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """处理未找到"""
        return jsonify({
            'success': False,
            'data': None,
            'message': '请求的资源不存在'
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        """处理方法不允许"""
        return jsonify({
            'success': False,
            'data': None,
            'message': '请求方法不允许'
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        """处理内部错误"""
        logger.error(f"服务器内部错误: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'data': None,
            'message': '服务器内部错误，请稍后重试'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        """处理其他异常"""
        # 记录详细错误信息
        logger.critical(
            f"未处理的异常: {type(e).__name__}: {str(e)}",
            exc_info=True
        )
        
        # 生产环境不暴露详细错误信息
        return jsonify({
            'success': False,
            'data': None,
            'message': '服务器内部错误，请稍后重试'
        }), 500
