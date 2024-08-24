from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List as TypingList, Optional
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

class Memo(BaseModel):
    id: str
    content: str

memos: TypingList[Memo] = []

app = FastAPI()

@app.post("/memos")
def create_memo(memo: Memo):
    memos.append(memo)
    return '메모 추가에 성공했습니다.'

@app.get("/memos")
def read_memo(sort_by: Optional[str] = Query(None, description="Sort by 'alphabetical' or 'registration'")):
    if sort_by == "alphabetical":
        sorted_memos = sorted(memos, key=lambda m: m.content)
    elif sort_by == "registration":
        sorted_memos = memos 
    else:
        sorted_memos = memos  
    
    return sorted_memos

@app.put("/memos/{id}")
def put_memo(id: str, req_memo: Memo):
    for memo in memos:
        if memo.id == id:
            memo.content = req_memo.content
            return "성공했습니다."
    return "그런 메모는 없습니다"

@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: str):
    for index, memo in enumerate(memos):
        if memo.id == memo_id:
            memos.pop(index)
            return "성공했습니다."
    return "그런 메모는 없습니다"

app.mount("/", StaticFiles(directory="static", html=True), name="static")

    
