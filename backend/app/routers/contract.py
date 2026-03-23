from fastapi import APIRouter

from app.models.schemas import ContractReviewRequest, ContractReviewResponse
from app.services.contract_service import ContractReviewService


router = APIRouter(prefix="/api/contract", tags=["contract"])
contract_service = ContractReviewService()


@router.post("/review", response_model=ContractReviewResponse)
async def review_contract(request: ContractReviewRequest) -> ContractReviewResponse:
    return await contract_service.review(request)
