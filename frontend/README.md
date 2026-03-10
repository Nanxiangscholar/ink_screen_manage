# 水墨屏数据管理系统 - 前端

## 技术栈

- Vue 3
- Vue Router
- Element Plus
- Axios

## 安装

1. 确保已安装 Node.js 和 npm
   - 下载地址：https://nodejs.org/en/download/

2. 安装依赖

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

## 运行

```bash
# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 项目结构

```
frontend/
├── public/            # 静态资源
├── src/
│   ├── assets/        # 资源文件
│   ├── components/    # 组件
│   ├── views/         # 页面
│   ├── router/        # 路由配置
│   ├── main.js        # 入口文件
│   └── App.vue        # 根组件
├── index.html         # HTML 模板
├── package.json       # 项目配置
└── vite.config.js     # Vite 配置
```

## 主要页面

- **登录页**：用户登录系统
- **首页**：系统概览，包含侧边导航
- **产品管理**：管理产品信息
- **电子标签**：管理电子标签的绑定、解绑和状态
- **字段管理**：管理系统字段配置

## API 接口

前端通过以下 API 接口与后端通信：

### 认证
- `POST /api/login` - 登录

### 产品管理
- `GET /api/products` - 获取产品列表
- `POST /api/products` - 添加产品
- `PUT /api/products/:id` - 更新产品
- `DELETE /api/products/:id` - 删除产品

### 电子标签
- `GET /api/esl` - 获取电子标签列表
- `POST /api/esl/bind` - 绑定标签
- `POST /api/esl/unbind` - 解绑标签
- `POST /api/esl/refresh` - 刷新标签
- `GET /api/esl/status/:id` - 检查标签状态

### 字段管理
- `GET /api/fields` - 获取字段列表
- `POST /api/fields` - 添加字段
- `PUT /api/fields/:id` - 更新字段
- `DELETE /api/fields/:id` - 删除字段

## 开发说明

1. 开发时，Vite 会将 API 请求代理到 `http://localhost:80`
2. 构建生产版本时，静态文件会输出到 `../app/static/vue` 目录
3. 前端使用 Element Plus 组件库，提供统一的 UI 风格
4. 路由使用 Vue Router，实现页面跳转
5. 数据请求使用 Axios，与后端 API 通信
