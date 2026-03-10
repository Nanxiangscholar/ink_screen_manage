import pymysql
from pymysql import Error

def create_db_connection(database_name='goods'):
    """创建数据库连接
    
    Args:
        database_name: 数据库名称，默认为'goods'
    
    Returns:
        数据库连接对象或None
    """
    try:
        connection = pymysql.connect(
            host='20.203.201.251',
            port=3307,
            database=database_name,
            user='root',
            password='root',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Error as e:
        print(f"连接{database_name}数据库时出错: {e}")
        return None

# 为了保持兼容性，提供特定数据库的连接函数
def create_store_db_connection():
    """创建storedb数据库连接"""
    return create_db_connection('storedb')

def create_eslworking_connection():
    """创建eslworking数据库连接"""
    return create_db_connection('eslworking')