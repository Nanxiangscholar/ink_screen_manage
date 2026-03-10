from .base import BaseModel, db


class User(BaseModel):
    """用户模型"""
    __tablename__ = 'user'
    
    username = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, index=True)
    user_id = db.Column(db.String(50), nullable=False, index=True)
    
    __table_args__ = (
        db.Index('idx_user_role_userid', 'role', 'user_id'),
    )
    
    def to_dict(self):
        """转换为字典"""
        return {
            'username': self.username,
            'role': self.role,
            'user_id': self.user_id
        }
