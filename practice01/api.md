# 实验报告自评辅助系统 API 文档 (api.md)

## 1. 概述
- **基础路径**: `/api/v1`
- **认证方式**: 请求头 `Authorization: Bearer <JWT>`
- **角色**: `student`（默认）、`teacher`、`admin`
- **数据格式**: 请求/响应体均为 JSON

---

## 2. 认证模块

### 2.1 登录
**`POST /auth/login`**

请求体：
```json
{
  "student_id": "24068240235",
  "password": "123456"
}