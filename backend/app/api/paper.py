from fastapi import APIRouter, status, Depends
from app.schemas.paper import FetchRequest, PaperProcessResponse
from app.services.arxiv_service import ArxivService
from app.services.llm_service import LLMService
router = APIRouter()

def get_llm_service() -> LLMService:
    return LLMService()

@router.post(
    "/process-paper", 
    response_model=PaperProcessResponse, 
    status_code=status.HTTP_200_OK,
    summary="Process and analyze an arXiv research paper"
)
async def process_paper(
    request: FetchRequest, 
    llm_service: LLMService = Depends(get_llm_service)
):
    # 1. Fetch metadata and URL
    metadata, pdf_url = await ArxivService.fetch_paper_data(request.url_or_id)
    
    # 2. Extract context window text
    full_text = await ArxivService.extract_pdf_text(str(pdf_url))
    
    # 3. Process insights through LLM pipeline
    summary, methodology, study_notes = await llm_service.generate_insights(full_text)
    
    return PaperProcessResponse(
        metadata=metadata,
        summary=summary,
        methodology=methodology,
        study_notes=study_notes
    )
