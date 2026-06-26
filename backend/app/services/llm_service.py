from fastapi import HTTPException, status
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.core.config import settings

class LLMService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL, 
            temperature=settings.GEMINI_TEMPERATURE,
            google_api_key=settings.GEMINI_API_KEY
        )
        
        self.summary_template = PromptTemplate.from_template(
            "Summarize the following research paper concisely, highlighting its main contributions and core thesis:\n\n{text}"
        )
        self.method_template = PromptTemplate.from_template(
            "Analyze the following research paper text and extract the methodology, experimental setup, and dataset details used:\n\n{text}"
        )
        self.notes_template = PromptTemplate.from_template(
            "Transform the following research paper into comprehensive study notes. Use bullet points, bold key terms, and create a 'Key Takeaways' section:\n\n{text}"
        )

    async def generate_insights(self, full_text: str) -> tuple[str, str, str]:
        try:
            summary_chain = self.summary_template | self.llm
            method_chain = self.method_template | self.llm
            notes_chain = self.notes_template | self.llm
            
            summary = await summary_chain.ainvoke({"text": full_text})
            method = await method_chain.ainvoke({"text": full_text})
            notes = await notes_chain.ainvoke({"text": full_text})
            
            return summary.content, method.content, notes.content
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"LLM Generative Processing Error: {str(e)}"
            )