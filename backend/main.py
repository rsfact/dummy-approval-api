import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(docs_url="/docs", openapi_url="/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイルの設定
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("../frontend/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # 環境変数を HTML に挿入
    html_content = html_content.replace("__BACKEND_URL__", os.getenv("BACKEND_URL", "http://localhost:8000"))

    return HTMLResponse(content=html_content)

class Quote(BaseModel):
    id: int
    customer_id: Optional[str] = None
    customer: str
    amount: float
    created_date: str
    status: str
    final_approver: Optional[str] = None
    approval_date: Optional[str] = None

def load_data():
    # スクリプトのディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # JSONファイルへの絶対パスを作成
    json_path = os.path.join(script_dir, "quotes_data.json")

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Quote(**quote) for quote in data]
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"quotes_data.json file not found at {json_path}")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in quotes_data.json")

quotes_db = load_data()

@app.get("/pending-quotes", response_model=List[Quote])
async def get_pending_quotes():
    return [quote for quote in quotes_db if quote.status == "pending"]

@app.get("/waiting-quotes", response_model=List[Quote])
async def get_waiting_quotes():
    return [quote for quote in quotes_db if quote.status == "waiting"]

@app.get("/approved-quotes", response_model=List[Quote])
async def get_approved_quotes():
    return [quote for quote in quotes_db if quote.status == "approved"]

class ApprovalRequest(BaseModel):
    final_approver: str
    approval_date: str

@app.put("/start-approval/{quote_id}")
async def start_approval(quote_id: int):
    for quote in quotes_db:
        if quote.id == quote_id and quote.status == "waiting":
            quote.status = "pending"
            return {"message": "Quote moved to pending approval successfully"}
    raise HTTPException(status_code=404, detail="Waiting quote not found")

@app.put("/approve-quote/{quote_id}")
async def approve_quote(quote_id: int, approval: ApprovalRequest):
    for quote in quotes_db:
        if quote.id == quote_id and quote.status == "pending":
            quote.status = "approved"
            quote.final_approver = approval.final_approver
            quote.approval_date = approval.approval_date
            return {"message": "Quote approved successfully"}
    raise HTTPException(status_code=404, detail="Pending quote not found")

@app.post("/reset-data")
async def reset_data():
    global quotes_db
    quotes_db = load_data()
    for quote in quotes_db:
        quote.status = "waiting"
        quote.final_approver = None
        quote.approval_date = None
    return {"message": "Data reset successfully"}

@app.get("/all-quotes", response_model=List[Quote])
async def get_all_quotes():
    return quotes_db

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
