# 水墨屏数据管理系统 - API 接口文档

## 项目信息

- **项目名称**: 水墨屏数据管理系统
- **后端框架**: Flask
- **运行地址**: http://localhost:80
- **API 前缀**: `/api`

## 配置说明

项目依赖的环境变量：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `SECRET_KEY` | Session 加密密钥 | dev-secret-key-change-in-production |
| `DATABASE_URL` | 主数据库连接 | mysql+pymysql://root:root@20.203.201.251:3307/goods |
| `DATABASE_URL_STOREDB` | storedb 数据库连接 | mysql+pymysql://root:root@20.203.201.251:3307/storedb |
| `DATABASE_URL_ESLWORKING` | eslworking 数据库连接 | mysql+pymysql://root:root@20.203.201.251:3307/eslworking |
| `PRISMART_BASE_URL` | PrismArt 服务地址 | http://20.203.201.251:8090 |
| `PRISMART_USERNAME` | PrismArt 用户名 | hs-admin |
| `PRISMART_PASSWORD` | PrismArt 密码 | 000000 |
| `PRISMART_CUSTOMER_CODE` | PrismArt 客户代码 | hs |
| `PRISMART_STORE_CODE` | PrismArt 店铺代码 | 101 |
| `INVITATION_CODE` | 邀请码 | jushi |

---

## 认证接口 (Authentication)

### 1. 用户登录

**请求**
```
POST /api/auth/login
```

**请求参数**
```json
{
  "username": "string",
  "password": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "username": "admin",
    "role": "admin",
    "user_id": 1
  }
}
```

---

### 2. 用户注册

**请求**
```
POST /api/auth/register
```

**请求参数**
```json
{
  "username": "string",
  "password": "string",
  "role": "string",
  "user_id": "string",
  "invitation_code": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "username": "newuser",
    "role": "user",
    "user_id": "12345"
  }
}
```

---

### 3. 用户登出

**请求**
```
POST /api/auth/logout
```

**请求头**
- 需要登录状态 (Session)

**响应示例**
```json
{
  "code": 200,
  "message": "登出成功",
  "data": {}
}
```

---

## 用户接口 (User)

### 1. 获取用户信息

**请求**
```
GET /api/user/info
```

**请求头**
- 需要登录状态 (Session)

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "username": "admin",
    "role": "admin",
    "user_id": 1
  }
}
```

---

### 2. 更新密码

**请求**
```
PUT /api/user/password
```

**请求头**
- 需要登录状态 (Session)

**请求参数**
```json
{
  "old_password": "string",
  "new_password": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "密码更新成功",
  "data": {}
}
```

---

## 产品管理接口 (Product)

### 1. 获取模板类型列表

**请求**
```
GET /api/product/template_types
```

**请求头**
- 需要登录状态 (Session)

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {"value": "21", "label": "拉丝"},
    {"value": "22", "label": "其他"}
  ]
}
```

---

### 2. 获取产品列表

**请求**
```
GET /api/product/products
```

**请求头**
- 需要登录状态 (Session)

**查询参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| store_code | string | 是 | 产线代码 |
| template_type | string | 否 | 模板类型 |

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "sku": "SKU001",
      "store_code": "lasiqu",
      "item_name": "产品名称",
      "brand": "品牌名",
      "unit": "个",
      "promo_reason": "21"
    }
  ]
}
```

---

### 3. 获取产品详情

**请求**
```
GET /api/product/product
```

**请求头**
- 需要登录状态 (Session)

**查询参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sku | string | 是 | 产品 SKU |
| store_code | string | 是 | 产线代码 |

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "sku": "SKU001",
    "store_code": "lasiqu",
    "item_name": "产品名称",
    "brand": "品牌名",
    "unit": "个",
    "promo_reason": "21"
  }
}
```

---

### 4. 获取促销原因

**请求**
```
GET /api/product/promo_reason
```

**请求头**
- 需要登录状态 (Session)

**查询参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sku | string | 是 | 产品 SKU |
| store_code | string | 是 | 产线代码 |

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "promo_reason": "21"
  }
}
```

---

### 5. 保存产品

**请求**
```
POST /api/product/save
```

**请求头**
- 需要登录状态 (Session)

**请求参数**
```json
{
  "sku": "string",
  "store_code": "string",
  "item_name": "string",
  "brand": "string",
  "unit": "string",
  "promo_reason": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "保存成功",
  "data": {}
}
```

---

### 6. 删除产品

**请求**
```
POST /api/product/delete
```

**请求头**
- 需要登录状态 (Session)

**请求参数**
```json
{
  "sku": "string",
  "store_code": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "删除成功",
  "data": {}
}
```

---

### 7. 获取炉位信息

**请求**
```
GET /api/product/furnace_info
```

**请求头**
- 需要登录状态 (Session)

**查询参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| store_code | string | 是 | 产线代码 |

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": [...]
}
```

---

## 电子标签接口 (ESL)

### 1. 获取 ESL 商品绑定信息

**请求**
```
GET /api/esl/goods
```

**请求头**
- 需要登录状态 (Session)

**查询参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sku | string | 否 | 产品 SKU |
| esl_id | string | 否 | 标签 ID |

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": [...]
}
```

---

### 2. 绑定标签到商品

**请求**
```
POST /api/esl/bind
```

**请求头**
- 需要登录状态 (Session)

**请求参数**
```json
{
  "esl_id": "string",
  "sku": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "绑定成功",
  "data": {}
}
```

---

### 3. 解绑标签

**请求**
```
POST /api/esl/unbind
```

**请求头**
- 需要登录状态 (Session)

**请求参数**
```json
{
  "esl_id": "string",
  "sku": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "解绑成功",
  "data": {}
}
```

---

### 4. 获取所有电子标签 ID

**请求**
```
GET /api/esl/ids
```

**请求头**
- 需要登录状态 (Session)

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": ["123456", "789012", ...]
}
```

---

### 5. 获取 SKU 列表

**请求**
```
GET /api/esl/skus
```

**请求头**
- 需要登录状态 (Session)

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": ["SKU001", "SKU002", ...]
}
```

---

### 6. 批量获取标签状态

**请求**
```
POST /api/esl/status
```

**请求头**
- 需要登录状态 (Session)

**请求参数**
```json
{
  "esl_ids": ["123456", "789012"]
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "123456": {"status": "online", "battery": 80},
    "789012": {"status": "offline", "battery": 20}
  }
}
```

---

## 字段管理接口 (Field)

### 1. 获取表字段和标签映射

**请求**
```
GET /api/field/table_fields
```

**请求头**
- 需要登录状态 (Session)

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "fields": [...],
    "label_mappings": [...]
  }
}
```

---

### 2. 更新字段标签

**请求**
```
POST /api/field/update_label
```

**请求头**
- 需要登录状态 (Session)

**请求参数**
```json
{
  "field_name": "string",
  "label": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {}
}
```

---

### 3. 获取模板字段映射

**请求**
```
GET /api/field/template_fields
```

**请求头**
- 需要登录状态 (Session)

**查询参数**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| promo_reason | string | 是 | 模板类型 |

**响应示例**
```json
{
  "code": 200,
  "message": "success",
  "data": [...]
}
```

---

### 4. 更新模板字段映射

**请求**
```
POST /api/field/update_template_field
```

**请求头**
- 需要登录状态 (Session)

**请求参数**
```json
{
  "field_name": "string",
  "label": "string",
  "promo_reason": "string",
  "promo_reason_label": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {}
}
```

---

### 5. 删除模板字段映射

**请求**
```
POST /api/field/delete_template_field
```

**请求头**
- 需要登录状态 (Session)

**请求参数**
```json
{
  "field_name": "string",
  "promo_reason": "string"
}
```

**响应示例**
```json
{
  "code": 200,
  "message": "删除成功",
  "data": {}
}
```

---

## Vue 前端接口 (兼容层)

以下接口为 Vue 前端提供的兼容 API：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/products | 获取产品列表 (分页) |
| GET | /api/products/:id | 获取产品详情 |
| POST | /api/products | 添加产品 |
| PUT | /api/products/:id | 更新产品 |
| DELETE | /api/products/:id | 删除产品 |
| GET | /api/esl | 获取电子标签列表 (分页) |
| POST | /api/esl/bind | 绑定电子标签 |
| POST | /api/esl/unbind | 解绑电子标签 |
| POST | /api/esl/refresh | 刷新电子标签 |
| GET | /api/esl/status/:id | 检查标签状态 |
| GET | /api/fields | 获取字段列表 (分页) |
| POST | /api/fields | 添加字段 |
| PUT | /api/fields/:id | 更新字段 |
| DELETE | /api/fields/:id | 删除字段 |
| POST | /api/login | 登录 (Vue 前端) |

---

## 响应格式说明

### 成功响应
```json
{
  "code": 200,
  "message": "success",
  "data": {...}
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "错误信息",
  "data": null
}
```

---

## 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未登录/认证失败 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

