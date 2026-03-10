from flask import Blueprint

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
def index():
    """首页"""
    return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>水墨屏数据管理系统</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f7fa;
            }
            .container {
                max-width: 800px;
                margin: 100px auto;
                padding: 20px;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #409eff;
                text-align: center;
            }
            p {
                text-align: center;
                color: #606266;
                font-size: 16px;
            }
            .api-info {
                margin-top: 30px;
                padding: 20px;
                background-color: #ecf5ff;
                border-radius: 4px;
            }
            .api-item {
                margin: 10px 0;
                padding: 10px;
                background-color: white;
                border-radius: 4px;
                border-left: 4px solid #409eff;
            }
            .api-item h3 {
                margin: 0 0 5px 0;
                color: #303133;
            }
            .api-item p {
                margin: 0;
                color: #606266;
                font-size: 14px;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>水墨屏数据管理系统</h1>
            <p>后端服务已成功启动！</p>
            <p>前端项目正在构建中...</p>
            
            <div class="api-info">
                <h2>API 接口信息</h2>
                
                <div class="api-item">
                    <h3>认证接口</h3>
                    <p>POST /api/login - 用户登录</p>
                </div>
                
                <div class="api-item">
                    <h3>产品管理</h3>
                    <p>GET /api/products - 获取产品列表</p>
                    <p>POST /api/products - 添加产品</p>
                    <p>PUT /api/products/:id - 更新产品</p>
                    <p>DELETE /api/products/:id - 删除产品</p>
                </div>
                
                <div class="api-item">
                    <h3>电子标签</h3>
                    <p>GET /api/esl - 获取电子标签列表</p>
                    <p>POST /api/esl/bind - 绑定标签</p>
                    <p>POST /api/esl/unbind - 解绑标签</p>
                    <p>POST /api/esl/refresh - 刷新标签</p>
                    <p>GET /api/esl/status/:id - 检查标签状态</p>
                </div>
                
                <div class="api-item">
                    <h3>字段管理</h3>
                    <p>GET /api/fields - 获取字段列表</p>
                    <p>POST /api/fields - 添加字段</p>
                    <p>PUT /api/fields/:id - 更新字段</p>
                    <p>DELETE /api/fields/:id - 删除字段</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''


@routes_bp.route('/health')
def health_check():
    """健康检查"""
    return {'status': 'ok', 'message': '服务运行正常'}
