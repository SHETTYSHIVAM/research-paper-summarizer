import re
import arxiv
from app.core.logging import logger

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

class ArxivClient:

    @staticmethod
    def get_paper(arxiv_id: str):
        clean_id = extract_arxiv_id(arxiv_id)
        logger.debug(f"Parsed arXiv ID '{clean_id}' from input '{arxiv_id}'")
        client = arxiv.Client()
        search = arxiv.Search(id_list=[clean_id])
        try:
            return next(client.results(search))
        except StopIteration:
            return None