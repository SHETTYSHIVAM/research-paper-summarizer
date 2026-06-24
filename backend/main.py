from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.paper import router as paper_router
app = FastAPI(title="Research Paper Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)

app.include_router(paper_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
