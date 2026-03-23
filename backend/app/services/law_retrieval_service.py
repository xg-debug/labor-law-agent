import logging

from app.models.schemas import LawReference


logger = logging.getLogger(__name__)


LAW_LIBRARY: dict[str, list[LawReference]] = {
    "dismissal": [
        LawReference(
            name="《劳动合同法》第三十九条",
            summary="劳动者在试用期间被证明不符合录用条件的，用人单位可以解除劳动合同。",
            source="法律条文",
        ),
        LawReference(
            name="《劳动合同法》第八十七条",
            summary="违法解除劳动合同的，应当支付赔偿金。",
            source="法律条文",
        ),
    ],
    "overtime": [
        LawReference(
            name="《劳动法》第四十四条",
            summary="安排加班的，应按法定标准支付加班工资。",
            source="法律条文",
        ),
        LawReference(
            name="《工资支付暂行规定》第十三条",
            summary="用人单位依法安排劳动者延长工作时间，应支付不低于法定标准的工资报酬。",
            source="法律条文",
        ),
    ],
    "unsigned_contract": [
        LawReference(
            name="《劳动合同法》第八十二条",
            summary="用工超过一个月不满一年未订立书面劳动合同，应向劳动者每月支付二倍工资。",
            source="法律条文",
        )
    ],
    "contract_review": [
        LawReference(
            name="《劳动合同法》第十九条",
            summary="试用期期限与劳动合同期限应对应，不得超过法定上限。",
            source="法律条文",
        ),
        LawReference(
            name="《劳动合同法》第二十条",
            summary="试用期工资不得低于本单位相同岗位最低档工资或者劳动合同约定工资的80%。",
            source="法律条文",
        ),
    ],
}


class LawRetrievalService:
    async def search(self, keyword: str, scene: str, summary: str = "") -> list[LawReference]:
        logger.info("law_search scene=%s keyword=%s", scene, keyword)
        if scene == "contract_review":
            return LAW_LIBRARY["contract_review"]
        if "辞退" in keyword or "解除" in keyword:
            return LAW_LIBRARY["dismissal"]
        if "加班" in keyword:
            return LAW_LIBRARY["overtime"]
        if "没签" in keyword or "未签" in keyword:
            return LAW_LIBRARY["unsigned_contract"]
        return LAW_LIBRARY["dismissal"]
