from langchain_community.document_loaders import PyPDFLoader


class PDFService:

    @staticmethod
    def load_text(pdf_url: str) -> str:
        loader = PyPDFLoader(pdf_url)

        docs = loader.load()

        return "\n".join(
            doc.page_content
            for doc in docs[:20]
        )