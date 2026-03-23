import logging
import os


logger = logging.getLogger(__name__)


class LLMService:
    """
    统一 LLM 调用封装。
    当前实现为可离线运行的占位版本，便于本地联调。
    后续可在此接入任意模型供应商。
    """

    def __init__(self) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "mock")
        self.model = os.getenv("LLM_MODEL", "labor-law-agent-v1")

    async def generate(self, prompt: str, payload: dict) -> str:
        logger.info(
            "llm_generate provider=%s model=%s payload_keys=%s",
            self.provider,
            self.model,
            list(payload.keys()),
        )
        question = payload.get("question") or payload.get("facts") or "劳动法场景分析"
        return f"【模型输出草稿】已根据输入内容完成分析：{question[:120]}"
