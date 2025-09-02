import os
import uuid
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np

from .document_processor import DocumentChunk

class VectorStore:
    def __init__(self):
        self.chroma_db_path = os.getenv("CHROMA_DB_PATH", "./vector_db")
        os.makedirs(self.chroma_db_path, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=self.chroma_db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add_documents(self, chunks: List[DocumentChunk], collection_name: str = "default") -> int:
        try:
            collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": f"Document collection: {collection_name}"}
            )
            
            documents = []
            embeddings = []
            metadatas = []
            ids = []
            
            for chunk in chunks:
                doc_id = str(uuid.uuid4())
                embedding = self.embedding_model.encode(chunk.content).tolist()
                
                documents.append(chunk.content)
                embeddings.append(embedding)
                metadatas.append(chunk.metadata)
                ids.append(doc_id)
            
            collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            return len(documents)
            
        except Exception as e:
            print(f"문서 추가 중 오류 발생: {str(e)}")
            return 0
    
    def search_similar_documents(
        self, 
        query: str, 
        collection_name: str = "default", 
        n_results: int = 5
    ) -> List[Dict[str, Any]]:
        try:
            collection = self.client.get_collection(collection_name)
            
            query_embedding = self.embedding_model.encode(query).tolist()
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            similar_docs = []
            if results['documents'] and len(results['documents'][0]) > 0:
                for i in range(len(results['documents'][0])):
                    similar_docs.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'similarity': 1 - results['distances'][0][i] if results['distances'] else 1.0
                    })
            
            return similar_docs
            
        except Exception as e:
            print(f"문서 검색 중 오류 발생: {str(e)}")
            return []
    
    def list_collections(self) -> List[str]:
        try:
            collections = self.client.list_collections()
            return [collection.name for collection in collections]
        except Exception as e:
            print(f"컬렉션 목록 조회 중 오류 발생: {str(e)}")
            return []
    
    def delete_collection(self, collection_name: str) -> bool:
        try:
            self.client.delete_collection(collection_name)
            return True
        except Exception as e:
            print(f"컬렉션 삭제 중 오류 발생: {str(e)}")
            return False
    
    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        try:
            collection = self.client.get_collection(collection_name)
            count = collection.count()
            
            return {
                "name": collection_name,
                "count": count,
                "metadata": collection.metadata
            }
        except Exception as e:
            print(f"컬렉션 정보 조회 중 오류 발생: {str(e)}")
            return {}
    
    def get_embedding_dimension(self) -> int:
        sample_text = "테스트 텍스트"
        embedding = self.embedding_model.encode(sample_text)
        return len(embedding)