import logging

from app.models.schemas import ContractReviewRequest, ContractReviewResponse, RiskItem
from app.prompts.templates import CONTRACT_REVIEW_PROMPT_TEMPLATE
from app.services.law_retrieval_service import LawRetrievalService
from app.services.llm_service import LLMService


logger = logging.getLogger(__name__)


class ContractReviewService:
    def __init__(self) -> None:
        self.llm_service = LLMService()
        self.law_service = LawRetrievalService()

    @staticmethod
    def _detect_contract_type(text: str) -> str:
        if "无固定期限" in text:
            return "无固定期限劳动合同"
        if "劳务协议" in text:
            return "劳务协议"
        return "固定期限劳动合同"

    async def review(self, request: ContractReviewRequest) -> ContractReviewResponse:
        contract_text = request.contract_text.strip()
        logger.info("contract_review text_length=%d", len(contract_text))

        _ = await self.llm_service.generate(
            prompt=CONTRACT_REVIEW_PROMPT_TEMPLATE,
            payload={"contract_text": contract_text[:3000]},
        )
        law_references = await self.law_service.search(
            keyword=contract_text[:80],
            scene="contract_review",
        )

        risks: list[RiskItem] = []
        if "试用期6个月" in contract_text or "试用期六个月" in contract_text:
            risks.append(
                RiskItem(
                    title="试用期条款可能超法定上限",
                    level="高",
                    description="试用期约定过长，可能违反劳动合同法关于试用期期限的规定。",
                    suggestion="根据合同期限重新设定试用期，避免超过法定上限。",
                )
            )
        if "不支付加班费" in contract_text or "加班费包含在工资内" in contract_text:
            risks.append(
                RiskItem(
                    title="加班工资条款违法风险",
                    level="高",
                    description="以固定工资涵盖全部加班费或约定不支付加班费，存在违法风险。",
                    suggestion="补充合法加班费计算与支付规则，并明确审批流程。",
                )
            )
        if "社会保险由员工自行缴纳" in contract_text:
            risks.append(
                RiskItem(
                    title="社保条款不合规",
                    level="中",
                    description="约定由劳动者自行承担缴纳义务，存在合规风险。",
                    suggestion="按法律规定由单位依法办理社保登记并缴纳。",
                )
            )
        if not risks:
            risks.append(
                RiskItem(
                    title="部分核心条款表达不完整",
                    level="中",
                    description="合同未明确工资构成、加班规则、解除流程等关键信息。",
                    suggestion="补充标准条款并固化通知、审批、送达流程。",
                )
            )

        return ContractReviewResponse(
            contract_type=self._detect_contract_type(contract_text),
            review_items=["试用期条款", "工资与加班条款", "社保条款", "解除劳动关系条款"],
            risks=risks,
            suggestions=[
                "按劳动合同法补齐试用期和工资条款",
                "明确加班审批、加班费和调休规则",
                "完善解除流程中的通知和证据留存机制",
            ],
            law_references=law_references,
        )
