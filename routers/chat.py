from fastapi import APIRouter

from pydantic import BaseModel

from rag.engine import run_agent

class Require(BaseModel):
    question: str

router = APIRouter()
@router.post("/chat")
async def chat(que: Require):
    response = run_agent(que.question)
    return response

