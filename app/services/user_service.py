from ..dao.user_dao import UserDAO
from passlib.hash import pbkdf2_sha256


class UserService:
    """用户服务"""
    
    @staticmethod
    def get_user_by_id(user_id):
        """根据ID获取用户"""
        return UserDAO.get_by_user_id(user_id)
    
    @staticmethod
    def update_password(user, old_password, new_password):
        """更新密码"""
        # 验证旧密码
        if not pbkdf2_sha256.verify(old_password, user.password):
            return False, "旧密码错误"
        
        # 加密新密码
        hashed_password = pbkdf2_sha256.hash(new_password)
        
        # 更新密码
        UserDAO.update(user, password=hashed_password)
        return True, "密码更新成功"
    
    @staticmethod
    def update_role(user, role):
        """更新用户角色"""
        UserDAO.update(user, role=role)
        return True, "角色更新成功"
