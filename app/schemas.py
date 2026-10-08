from pydantic import BaseModel

class HistoryItem(BaseModel):
    role:str
    content:str


class ChatRequest(BaseModel):
    question:str
    history:list[HistoryItem]=[]


class ChatResponse(BaseModel):
    answer:str
    sources:list[str|dict]=[]


