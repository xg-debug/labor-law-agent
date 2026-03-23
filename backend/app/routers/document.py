from fastapi import APIRouter

from app.models.schemas import DocumentGenerateRequest, DocumentGenerateResponse
from app.services.document_service import DocumentService


router = APIRouter(prefix="/api/document", tags=["document"])
document_service = DocumentService()


@router.post("/generate", response_model=DocumentGenerateResponse)
async def generate_document(request: DocumentGenerateRequest) -> DocumentGenerateResponse:
    return await document_service.generate(request)
