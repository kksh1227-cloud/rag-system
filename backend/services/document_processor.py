import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pypdf
from docx import Document

class DocumentChunk:
    def __init__(self, content: str, metadata: dict):
        self.content = content
        self.metadata = metadata

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def process_document(self, file_path: str) -> List[DocumentChunk]:
        file_extension = os.path.splitext(file_path)[1].lower()
        filename = os.path.basename(file_path)
        
        if file_extension == '.pdf':
            content = self._extract_pdf_content(file_path)
        elif file_extension == '.docx':
            content = self._extract_docx_content(file_path)
        elif file_extension == '.txt':
            content = self._extract_txt_content(file_path)
        else:
            raise ValueError(f"지원하지 않는 파일 형식: {file_extension}")
        
        if not content.strip():
            raise ValueError("문서에서 텍스트를 추출할 수 없습니다.")
        
        text_chunks = self.text_splitter.split_text(content)
        
        chunks = []
        for i, chunk_content in enumerate(text_chunks):
            metadata = {
                "filename": filename,
                "file_path": file_path,
                "chunk_index": i,
                "total_chunks": len(text_chunks),
                "file_type": file_extension
            }
            chunks.append(DocumentChunk(chunk_content, metadata))
        
        return chunks
    
    def _extract_pdf_content(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as file:
                reader = pypdf.PdfReader(file)
                content = []
                
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        content.append(f"[페이지 {page_num + 1}]\n{text}")
                
                return "\n\n".join(content)
        except Exception as e:
            raise ValueError(f"PDF 파일 읽기 오류: {str(e)}")
    
    def _extract_docx_content(self, file_path: str) -> str:
        try:
            doc = Document(file_path)
            content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    content.append(paragraph.text)
            
            return "\n\n".join(content)
        except Exception as e:
            raise ValueError(f"DOCX 파일 읽기 오류: {str(e)}")
    
    def _extract_txt_content(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='cp949') as file:
                    return file.read()
            except Exception as e:
                raise ValueError(f"TXT 파일 읽기 오류: {str(e)}")
        except Exception as e:
            raise ValueError(f"TXT 파일 읽기 오류: {str(e)}")
    
    def get_document_info(self, file_path: str) -> dict:
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        file_extension = os.path.splitext(file_path)[1].lower()
        
        return {
            "filename": filename,
            "file_size": file_size,
            "file_type": file_extension,
            "file_path": file_path
        }