from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from services.document_processor import DocumentProcessor
from services.vector_store import VectorStore
from services.rag_service import RAGService

load_dotenv()

app = FastAPI(
    title="RAG System API",
    description="문서 기반 질의응답 시스템",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

doc_processor = DocumentProcessor()
vector_store = VectorStore()
rag_service = RAGService(vector_store)

class ChatRequest(BaseModel):
    question: str
    collection_name: str = "default"

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float

@app.get("/")
async def root():
    return {"message": "RAG System API is running"}

@app.post("/upload", response_model=dict)
async def upload_document(
    file: UploadFile = File(...),
    collection_name: str = "default"
):
    try:
        if not file.filename.endswith(('.pdf', '.docx', '.txt')):
            raise HTTPException(
                status_code=400, 
                detail="지원하지 않는 파일 형식입니다. PDF, DOCX, TXT 파일만 업로드 가능합니다."
            )
        
        upload_dir = os.getenv("UPLOAD_DIR", "./documents")
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        chunks = doc_processor.process_document(file_path)
        
        success_count = vector_store.add_documents(chunks, collection_name)
        
        return {
            "message": f"문서가 성공적으로 업로드되었습니다.",
            "filename": file.filename,
            "chunks_count": len(chunks),
            "stored_count": success_count,
            "collection": collection_name
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"문서 처리 중 오류가 발생했습니다: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await rag_service.get_answer(
            question=request.question,
            collection_name=request.collection_name
        )
        
        return ChatResponse(
            answer=response["answer"],
            sources=response["sources"],
            confidence=response["confidence"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"답변 생성 중 오류가 발생했습니다: {str(e)}")

@app.get("/collections")
async def list_collections():
    try:
        collections = vector_store.list_collections()
        return {"collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"컬렉션 조회 중 오류가 발생했습니다: {str(e)}")

@app.delete("/collections/{collection_name}")
async def delete_collection(collection_name: str):
    try:
        success = vector_store.delete_collection(collection_name)
        if success:
            return {"message": f"컬렉션 '{collection_name}'이 삭제되었습니다."}
        else:
            raise HTTPException(status_code=404, detail="컬렉션을 찾을 수 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"컬렉션 삭제 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(app, host=host, port=port, reload=debug)