from ..dao.user_dao import UserDAO
from ..dao import user_dao
from passlib.hash import pbkdf2_sha256
from ..utils.logger import logger
from ..config import get_config


class AuthService:
    """认证服务"""
    
    @staticmethod
    def _get_invitation_code() -> str:
        """获取邀请码"""
        return get_config().INVITATION_CODE
    
    @staticmethod
    def login(username, password):
        """用户登录"""
        user = UserDAO.get_by_username(username)
        if not user:
            return None, "用户不存在"
        
        # 验证密码
        if not pbkdf2_sha256.verify(password, user.password):
            logger.warning(f"用户 {username} 登录失败：密码错误")
            return None, "密码错误"
        
        logger.info(f"用户 {username} 登录成功")
        return user, "登录成功"
    
    @staticmethod
    def validate_user_credentials(username, password, check_exists=False):
        """
        验证用户名和密码是否符合要求
        返回错误信息，如果没有错误则返回None
        """
        # 用户名验证
        if not username:
            return '用户名不能为空'
        
        if len(username) < 3:
            return '用户名至少需要3个字符'
        
        if len(username) > 20:
            return '用户名不能超过20个字符'
        
        if not username.replace('_', '').isalnum():
            return '用户名只能包含字母、数字和下划线'
        
        # 如果需要检查用户名是否存在
        if check_exists:
            existing_user = UserDAO.get_by_username(username)
            if existing_user:
                return '用户名已存在，请选择其他用户名'
        
        # 密码验证
        if not password:
            return '密码不能为空'
        
        if len(password) < 6:
            return '密码至少需要6个字符'
        
        if len(password) > 50:
            return '密码不能超过50个字符'
        
        # 检查是否包含至少一个字母和一个数字
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_letter and has_digit):
            return '密码必须包含至少一个字母和一个数字'
        
        return None  # 没有错误
    
    @staticmethod
    def validate_role(role):
        """验证角色是否有效"""
        valid_roles = ['admin', 'user', 'lasiqu_user', 'huagong_user']
        if role not in valid_roles:
            return f'无效的角色，允许的角色: {", ".join(valid_roles)}'
        return None
    
    @staticmethod
    def register(username, password, role, user_id, invitation_code):
        """用户注册"""
        # 验证邀请码
        if invitation_code != AuthService._get_invitation_code():
            logger.warning(f"注册失败：无效的邀请码")
            return None, "无效的邀请码"
        
        # 验证角色
        role_error = AuthService.validate_role(role)
        if role_error:
            return None, role_error
        
        # 验证用户名和密码
        validation_error = AuthService.validate_user_credentials(username, password, check_exists=True)
        if validation_error:
            return None, validation_error
        
        # 密码加密
        hashed_password = pbkdf2_sha256.hash(password)
        
        # 创建用户
        user = UserDAO.create(
            username=username,
            password=hashed_password,
            role=role,
            user_id=user_id
        )
        
        # 记录注册操作日志
        logger.info(f"新用户注册: {username}, 角色: {role}, 用户ID: {user_id}")
        
        return user, "注册成功"
