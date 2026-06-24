from pydantic import BaseModel
from typing import List

class FetchSchema(BaseModel):
    url_or_id: str



class PaperMetadata(BaseModel):
    title: str
    authors: List[str]
    published: str
    pdf_url: str


class PaperResponse(BaseModel):
    metadata: PaperMetadata
    summary: str
    methodology: str
    study_notes: str