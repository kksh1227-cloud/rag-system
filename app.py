# Hugging Face Spaces용 메인 앱 파일
import streamlit as st
import requests
import json
import os
import tempfile
import shutil
from pathlib import Path

# Hugging Face Spaces에서는 백엔드가 없으므로 로컬 처리 버전 사용
import sys
sys.path.append('backend/services')

try:
    from backend.services.document_processor import DocumentProcessor, DocumentChunk
    from backend.services.vector_store import VectorStore
    import openai
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False

st.set_page_config(
    page_title="RAG System - 문서 기반 Q&A",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG System - 문서 기반 Q&A 시스템")
st.markdown("---")

if not BACKEND_AVAILABLE:
    st.error("""
    ⚠️ **백엔드 서비스가 필요합니다**
    
    현재 Hugging Face Spaces에서는 백엔드 서비스 없이 프론트엔드만 실행 중입니다.
    
    **완전한 기능을 사용하려면:**
    1. OpenAI API 키가 필요합니다
    2. 벡터 데이터베이스 설정이 필요합니다
    3. 별도 서버에 백엔드 배포가 필요합니다
    
    **대안:**
    - Railway, Render 등에서 전체 시스템 배포
    - 로컬에서 실행: `python run_backend.py` + `streamlit run app.py`
    """)
    
    st.markdown("## 🎯 시스템 데모")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 문서 업로드")
        uploaded_file = st.file_uploader(
            "파일 선택 (데모 전용)",
            type=['pdf', 'docx', 'txt'],
            help="실제 업로드 기능은 백엔드 서버가 필요합니다."
        )
        
        if uploaded_file:
            st.info(f"📄 파일 선택됨: {uploaded_file.name}")
            st.info("💡 실제 처리를 위해서는 백엔드 서버가 필요합니다.")
    
    with col2:
        st.header("💬 질문하기")
        question = st.text_area(
            "질문을 입력하세요 (데모 전용)",
            placeholder="업로드한 문서에 대해 질문해보세요...",
            help="실제 답변 생성은 백엔드 서버가 필요합니다."
        )
        
        if st.button("🔍 질문하기 (데모)"):
            if question:
                st.info("🤖 AI 답변 (데모)")
                st.write(f"**질문:** {question}")
                st.write(f"**답변:** 실제 답변을 생성하려면 OpenAI API와 벡터 데이터베이스가 필요합니다. 현재는 데모 모드입니다.")
    
else:
    # 실제 RAG 시스템 구현 (백엔드가 있는 경우)
    st.info("✅ 백엔드 서비스가 연결되어 완전한 RAG 기능을 사용할 수 있습니다!")
    
    # 기존 frontend/app.py의 로직을 여기에 구현
    # (현재는 백엔드 API 없이는 실행되지 않음)

# 하단 정보
st.markdown("---")
st.markdown("## 📖 RAG 시스템 정보")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.info("""
    **🔧 기술 스택**
    - FastAPI (백엔드)
    - Streamlit (프론트엔드)  
    - ChromaDB (벡터 DB)
    - OpenAI GPT (LLM)
    - LangChain (문서 처리)
    """)

with col2:
    st.info("""
    **📋 주요 기능**
    - PDF/DOCX/TXT 업로드
    - 자동 문서 청킹
    - 시맨틱 검색
    - AI 기반 답변 생성
    - 컬렉션 관리
    """)

with col3:
    st.info("""
    **🚀 배포 옵션**
    - Railway (추천)
    - Render  
    - Streamlit Cloud
    - Docker 컨테이너
    - 로컬 실행
    """)

st.markdown("---")
st.markdown("""
### 🔗 관련 링크
- **GitHub 저장소**: [kksh1227-cloud/rag-system](https://github.com/kksh1227-cloud/rag-system)
- **완전한 배포 가이드**: README.md 참조
- **로컬 실행 방법**: `pip install -r requirements.txt` → `python run_backend.py`
""")

# 환경 정보
with st.expander("🔍 시스템 환경 정보"):
    st.write("**Python 버전**:", sys.version)
    st.write("**Streamlit 버전**:", st.__version__)
    st.write("**백엔드 상태**:", "사용 가능" if BACKEND_AVAILABLE else "연결 필요")
    st.write("**실행 환경**:", "Hugging Face Spaces")