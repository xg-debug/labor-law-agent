# Labor Law Agent Backend

## 运行

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

## 核心接口

- `GET /health`
- `POST /api/chat/ask`
- `POST /api/contract/review`
- `POST /api/document/generate`

## 说明

- 已包含统一错误处理、CORS、请求日志。
- `LLMService` 目前为离线可运行占位实现，后续可替换真实模型 API。
