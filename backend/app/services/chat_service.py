import logging

from app.models.schemas import ChatRequest, ChatResponse
from app.prompts.templates import CHAT_PROMPT_TEMPLATE
from app.services.law_retrieval_service import LawRetrievalService
from app.services.llm_service import LLMService


logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self) -> None:
        self.llm_service = LLMService()
        self.law_service = LawRetrievalService()

    @staticmethod
    def _extract_scene(question: str) -> str:
        if "加班" in question:
            return "overtime"
        if "没签" in question or "未签" in question:
            return "unsigned_contract"
        if "辞退" in question or "解除" in question:
            return "dismissal"
        return "general_labor"

    @staticmethod
    def _facts_from_question(question: str) -> list[str]:
        facts: list[str] = []
        if "试用期" in question:
            facts.append("当前场景涉及试用期")
        if "辞退" in question or "解除" in question:
            facts.append("存在劳动关系解除争议")
        if "加班" in question:
            facts.append("存在加班工资支付争议")
        if "没签" in question or "未签" in question:
            facts.append("存在未签书面劳动合同争议")
        if not facts:
            facts.append("需补充在职时间、岗位、工资标准、证据情况")
        return facts

    async def ask(self, request: ChatRequest) -> ChatResponse:
        scene = self._extract_scene(request.question)
        law_references = await self.law_service.search(
            keyword=request.question,
            scene=scene,
            summary=request.question[:80],
        )
        llm_text = await self.llm_service.generate(
            prompt=CHAT_PROMPT_TEMPLATE,
            payload={"question": request.question, "history": [m.model_dump() for m in request.history]},
        )
        logger.info("chat_scene=%s history_size=%d", scene, len(request.history))
        facts = self._facts_from_question(request.question)

        issues = [
            "用人单位行为是否合法",
            "是否应承担支付补偿或赔偿责任",
            "劳动者维权路径与证据是否充分",
        ]
        risk_tips = [
            "若事实证据不足，仲裁支持力度可能下降",
            "若超过仲裁时效，部分请求可能不被支持",
        ]
        suggestions = [
            "先固定证据：合同、工资流水、考勤记录、通知截图",
            "书面向单位主张权利并保留送达凭证",
            "必要时在时效内提起劳动仲裁",
        ]
        evidence = ["劳动合同/录用通知", "工资流水", "考勤与加班记录", "解除或沟通记录"]

        return ChatResponse(
            question_summary=f"围绕“{request.question[:30]}”的劳动法咨询分析",
            facts=facts,
            issues=issues,
            law_references=law_references,
            analysis=llm_text,
            conclusion="当前问题存在劳动争议风险，建议尽快补全事实与证据后推进维权。",
            risk_tips=risk_tips,
            suggestions=suggestions,
            evidence_list=evidence,
        )
