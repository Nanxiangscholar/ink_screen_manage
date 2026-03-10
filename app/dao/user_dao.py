from ..models.user import User
from ..models.base import db


class UserDAO:
    """用户数据访问层"""
    
    @staticmethod
    def get_by_username(username):
        """根据用户名获取用户"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_user_id(user_id):
        """根据用户ID获取用户"""
        return User.query.filter_by(user_id=user_id).first()
    
    @staticmethod
    def create(username, password, role, user_id):
        """创建用户"""
        user = User(
            username=username,
            password=password,
            role=role,
            user_id=user_id
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update(user, **kwargs):
        """更新用户信息"""
        for key, value in kwargs.items():
            setattr(user, key, value)
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user):
        """删除用户"""
        db.session.delete(user)
        db.session.commit()
