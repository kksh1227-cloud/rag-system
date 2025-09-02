import os
from typing import Dict, Any, List
import openai
from openai import OpenAI

from .vector_store import VectorStore

class RAGService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        self.system_prompt = """당신은 업로드된 문서를 기반으로 질문에 답하는 AI 어시스턴트입니다.

다음 지침을 따라주세요:
1. 제공된 문서 내용만을 기반으로 답변해주세요.
2. 문서에서 찾을 수 없는 정보는 "제공된 문서에서 해당 정보를 찾을 수 없습니다"라고 답변해주세요.
3. 답변은 한국어로 작성해주세요.
4. 가능한 한 구체적이고 정확한 답변을 제공해주세요.
5. 답변의 근거가 되는 문서의 부분을 명시해주세요."""

    async def get_answer(
        self, 
        question: str, 
        collection_name: str = "default",
        n_context_docs: int = 5
    ) -> Dict[str, Any]:
        try:
            similar_docs = self.vector_store.search_similar_documents(
                query=question,
                collection_name=collection_name,
                n_results=n_context_docs
            )
            
            if not similar_docs:
                return {
                    "answer": "관련 문서를 찾을 수 없습니다. 먼저 문서를 업로드해주세요.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            context = self._build_context(similar_docs)
            sources = self._extract_sources(similar_docs)
            
            prompt = self._build_prompt(question, context)
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            answer = response.choices[0].message.content
            confidence = self._calculate_confidence(similar_docs)
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence
            }
            
        except Exception as e:
            return {
                "answer": f"답변 생성 중 오류가 발생했습니다: {str(e)}",
                "sources": [],
                "confidence": 0.0
            }
    
    def _build_context(self, similar_docs: List[Dict[str, Any]]) -> str:
        context_parts = []
        for i, doc in enumerate(similar_docs, 1):
            filename = doc['metadata'].get('filename', 'Unknown')
            content = doc['content']
            context_parts.append(f"[문서 {i}: {filename}]\n{content}")
        
        return "\n\n".join(context_parts)
    
    def _build_prompt(self, question: str, context: str) -> str:
        return f"""다음은 업로드된 문서들의 내용입니다:

{context}

질문: {question}

위의 문서 내용을 바탕으로 질문에 답변해주세요. 답변의 근거가 되는 문서를 명시해주세요."""
    
    def _extract_sources(self, similar_docs: List[Dict[str, Any]]) -> List[str]:
        sources = []
        seen_files = set()
        
        for doc in similar_docs:
            filename = doc['metadata'].get('filename', 'Unknown')
            if filename not in seen_files:
                sources.append(filename)
                seen_files.add(filename)
        
        return sources
    
    def _calculate_confidence(self, similar_docs: List[Dict[str, Any]]) -> float:
        if not similar_docs:
            return 0.0
        
        similarities = [doc.get('similarity', 0.0) for doc in similar_docs]
        avg_similarity = sum(similarities) / len(similarities)
        
        return min(avg_similarity, 1.0)

class LocalRAGService(RAGService):
    """로컬 LLM을 사용하는 RAG 서비스 (예: Ollama)"""
    
    def __init__(self, vector_store: VectorStore, model_name: str = "llama2"):
        self.vector_store = vector_store
        self.model_name = model_name
        self.system_prompt = """당신은 업로드된 문서를 기반으로 질문에 답하는 AI 어시스턴트입니다.

다음 지침을 따라주세요:
1. 제공된 문서 내용만을 기반으로 답변해주세요.
2. 문서에서 찾을 수 없는 정보는 "제공된 문서에서 해당 정보를 찾을 수 없습니다"라고 답변해주세요.
3. 답변은 한국어로 작성해주세요.
4. 가능한 한 구체적이고 정확한 답변을 제공해주세요."""

    async def get_answer(
        self, 
        question: str, 
        collection_name: str = "default",
        n_context_docs: int = 5
    ) -> Dict[str, Any]:
        try:
            import requests
            
            similar_docs = self.vector_store.search_similar_documents(
                query=question,
                collection_name=collection_name,
                n_results=n_context_docs
            )
            
            if not similar_docs:
                return {
                    "answer": "관련 문서를 찾을 수 없습니다.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            context = self._build_context(similar_docs)
            sources = self._extract_sources(similar_docs)
            prompt = self._build_prompt(question, context)
            
            # Ollama API 호출
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': self.model_name,
                    'prompt': f"{self.system_prompt}\n\n{prompt}",
                    'stream': False
                }
            )
            
            if response.status_code == 200:
                answer = response.json().get('response', '답변을 생성할 수 없습니다.')
            else:
                answer = "로컬 LLM 서버에 연결할 수 없습니다."
            
            confidence = self._calculate_confidence(similar_docs)
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": confidence
            }
            
        except Exception as e:
            return {
                "answer": f"답변 생성 중 오류가 발생했습니다: {str(e)}",
                "sources": [],
                "confidence": 0.0
            }