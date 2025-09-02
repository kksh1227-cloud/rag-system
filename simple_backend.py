#!/usr/bin/env python3
"""
간단한 RAG 백엔드 API 서버
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI(
    title="RAG Backend API",
    description="간단한 문서 기반 질의응답 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    collection_name: str = "default"

class ChatResponse(BaseModel):
    answer: str
    sources: list = []
    confidence: float = 0.8

@app.get("/")
async def root():
    return {
        "message": "RAG Backend API is running!",
        "status": "healthy",
        "endpoints": ["/upload", "/chat", "/collections"]
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """문서 업로드 (데모 버전)"""
    return {
        "message": f"파일 '{file.filename}'이 성공적으로 업로드되었습니다.",
        "filename": file.filename,
        "size": f"{len(await file.read())} bytes",
        "status": "success"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """질의응답 (데모 버전)"""
    demo_answer = f"""
질문: {request.question}

답변: 현재는 데모 모드로 실행 중입니다. 

완전한 기능을 위해서는:
1. OpenAI API 키 설정
2. ChromaDB 벡터 저장소 연결
3. 문서 처리 파이프라인 활성화

가 필요합니다. 현재는 데모 응답을 제공하고 있습니다.
    """.strip()
    
    return ChatResponse(
        answer=demo_answer,
        sources=[f"demo_document.pdf"],
        confidence=0.8
    )

@app.get("/collections")
async def list_collections():
    """컬렉션 목록 조회"""
    return {
        "collections": ["default", "demo"],
        "total": 2
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)