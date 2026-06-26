import re
import arxiv
from fastapi import HTTPException, status
from fastapi.concurrency import run_in_threadpool
from langchain_community.document_loaders import PyPDFLoader
from app.core.config import settings
from app.schemas.paper import PaperMetadata

class ArxivService:
    def extract_arxiv_id(input_str: str) -> str:
        input_str = input_str.strip()
        
        # New ID pattern: digits, dot, digits, optional version
        # Old ID pattern: category/digits, optional version
        id_pattern_str = r"([a-zA-Z\-]+(?:\.[a-zA-Z\-]+)*/\d+(?:v\d+)?|\d+(?:\.\d+)+(?:v\d+)?)"
        
        # 1. Match DOI style: e.g. https://doi.org/10.48550/arXiv.2605.07903
        doi_match = re.search(r"doi\.org/10\.48550/arXiv\." + id_pattern_str, input_str, re.IGNORECASE)
        if doi_match:
            return doi_match.group(1)
            
        # 2. Match standard arxiv.org URLs: e.g. https://arxiv.org/abs/2605.07903
        url_match = re.search(r"arxiv\.org/(?:abs|pdf|html)/" + id_pattern_str, input_str, re.IGNORECASE)
        if url_match:
            return url_match.group(1)

        # 3. Match arXiv:XXXX.XXXX or arXiv:arch-ives/YYMMNNN
        prefix_match = re.search(r"arxiv:\s*" + id_pattern_str, input_str, re.IGNORECASE)
        if prefix_match:
            return prefix_match.group(1)

        # 4. If the string is exactly the ID pattern
        id_match = re.match(r"^(?:arxiv:)?" + id_pattern_str + r"$", input_str, re.IGNORECASE)
        if id_match:
            return id_match.group(1)

        # Fallback: search for the first match of the pattern anywhere in the string
        fallback_match = re.search(id_pattern_str, input_str)
        if fallback_match:
            return fallback_match.group(1)

        return input_str

    @classmethod
    async def fetch_paper_data(cls, url_or_id: str):
        arxiv_id = cls.extract_arxiv_id(url_or_id)
        
        # Run blocking arXiv API call in a separate worker thread
        client = arxiv.Client()
        search = arxiv.Search(id_list=[arxiv_id])
        try:
            paper = await run_in_threadpool(lambda: next(client.results(search)))
        except StopIteration:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Paper not found on arXiv"
            )

        metadata = PaperMetadata(
            title=paper.title,
            authors=[author.name for author in paper.authors],
            published=paper.published.strftime("%Y-%m-%d"),
            pdf_url=paper.pdf_url
        )
        
        return metadata, paper.pdf_url

    @staticmethod
    async def extract_pdf_text(pdf_url: str) -> str:
        """Loads PDF via Langchain on a background thread pool."""
        try:
            loader = PyPDFLoader(pdf_url)
            # PyPDFLoader.load() hits the network and parses disk/bytes; offload it.
            docs = await run_in_threadpool(loader.load)
            
            # Limit pages based on production configurations
            truncated_docs = docs[:settings.MAX_PDF_PAGES]
            return "\n".join([doc.page_content for doc in truncated_docs])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Failed to download or parse PDF document: {str(e)}"
            )