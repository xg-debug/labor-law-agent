# Labor Law Agent Frontend

技术栈：Vue 3 + Vite + Pinia + Element Plus + JavaScript

## 启动

```bash
cd frontend
npm install
npm run dev
```

## 构建

```bash
npm run build
npm run preview
```

## 环境变量

复制 `.env.example` 为 `.env`：

- `VITE_API_BASE_URL`：后端地址，默认 `http://localhost:8000`
- `VITE_API_TIMEOUT`：接口超时时间（毫秒）

## 页面说明

- `/` 首页：产品定位、核心能力、入口导航
- `/consult` 智能咨询：多轮问答、结构化结果、法律依据、跳转文书生成
- `/contract-review` 合同审查：文本输入、风险摘要/详细说明切换、风险卡片
- `/document-generate` 文书生成：类型选择、事实诉求输入、文书预览与复制

## 当前后端接口

- `GET /health`
- `POST /api/chat/ask`
- `POST /api/contract/review`
- `POST /api/document/generate`

页面已内置“示例数据”按钮，可在后端能力未接入前完成演示。
