import logging
from datetime import date

from app.models.schemas import DocumentGenerateRequest, DocumentGenerateResponse
from app.prompts.templates import DOCUMENT_GENERATE_PROMPT_TEMPLATE
from app.services.llm_service import LLMService


logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self) -> None:
        self.llm_service = LLMService()

    async def generate(self, request: DocumentGenerateRequest) -> DocumentGenerateResponse:
        logger.info("document_generate doc_type=%s", request.doc_type)
        _ = await self.llm_service.generate(
            prompt=DOCUMENT_GENERATE_PROMPT_TEMPLATE,
            payload=request.model_dump(),
        )

        today = date.today().isoformat()
        title = request.doc_type
        content = (
            f"{request.doc_type}\n\n"
            "申请人/发函人：________\n"
            "被申请人/收函人：________\n\n"
            f"事实概述：\n{request.facts}\n\n"
            f"主要诉求/用途：\n{request.claim}\n\n"
            "正文（可编辑）：\n"
            "1. 请根据真实时间线补全入职、履约、争议发生时间。\n"
            "2. 请根据证据材料补全金额、计算方式和法律依据。\n"
            "3. 请在落款处补全签名及日期。\n\n"
            f"生成日期：{today}\n"
        )

        return DocumentGenerateResponse(
            title=title,
            content=content,
            usage_notes="请在提交前核对主体信息、日期、金额与证据一致性，并由专业人员复核。",
            risk_tips=[
                "事实与证据不一致可能影响文书效力",
                "金额与请求事项应逐项可计算、可举证",
                "正式提交前建议进行律师复核",
            ],
        )
