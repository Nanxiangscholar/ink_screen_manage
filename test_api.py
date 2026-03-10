from app import create_app
import json

# 创建应用
app = create_app()

# 测试登录API
def test_login():
    with app.test_client() as client:
        # 测试登录
        response = client.post('/api/auth/login', 
                              data=json.dumps({'username': 'admin', 'password': 'admin123'}),
                              content_type='application/json')
        print(f"Login response: {response.status_code}")
        print(f"Login data: {response.get_json()}")

# 测试注册API
def test_register():
    with app.test_client() as client:
        # 测试注册（使用正确的邀请码）
        response = client.post('/api/auth/register', 
                              data=json.dumps({
                                  'username': 'testuser',
                                  'password': 'Test123456',
                                  'role': 'user',
                                  'user_id': 'testuser1',
                                  'invitation_code': 'jushi'
                              }),
                              content_type='application/json')
        print(f"Register response: {response.status_code}")
        print(f"Register data: {response.get_json()}")

# 测试产品列表API
def test_products():
    with app.test_client() as client:
        # 测试产品列表
        response = client.get('/api/products?store_code=lasiqu')
        print(f"Products response: {response.status_code}")
        print(f"Products data: {response.get_json()}")

# 测试健康检查API
def test_health():
    with app.test_client() as client:
        # 测试健康检查
        response = client.get('/health')
        print(f"Health response: {response.status_code}")
        print(f"Health data: {response.get_json()}")

if __name__ == '__main__':
    print("Testing API endpoints...")
    test_login()
    print("\n")
    test_register()
    print("\n")
    test_products()
    print("\n")
    test_health()