from fastapi import APIRouter
from app.db.schemas import FetchSchema
from app.clients.arxiv_client import ArxivClient
router = APIRouter()

@router.post("/process-paper")
async def process_paper(req: FetchSchema):
    arxiv_client = ArxivClient()
    paper = arxiv_client.get_paper(req.url_or_id)
    return {"paper": paper}
