from pydantic import BaseModel, Field, HttpUrl
from typing import List

class FetchRequest(BaseModel):
    url_or_id: str = Field(..., description="The arXiv paper ID or full abstract/PDF URL.")

class PaperMetadata(BaseModel):
    title: str
    authors: List[str]
    published: str
    pdf_url: HttpUrl

class PaperProcessResponse(BaseModel):
    metadata: PaperMetadata
    summary: str
    methodology: str
    study_notes: str