import streamlit as st
import requests
import json
import os
from pathlib import Path

st.set_page_config(
    page_title="RAG System - 문서 기반 Q&A",
    page_icon="📚",
    layout="wide"
)

API_BASE_URL = "http://localhost:8000"

def upload_file(file, collection_name):
    files = {"file": (file.name, file, file.type)}
    data = {"collection_name": collection_name}
    
    response = requests.post(f"{API_BASE_URL}/upload", files=files, data=data)
    return response.json()

def chat_with_rag(question, collection_name):
    data = {
        "question": question,
        "collection_name": collection_name
    }
    response = requests.post(f"{API_BASE_URL}/chat", json=data)
    return response.json()

def get_collections():
    try:
        response = requests.get(f"{API_BASE_URL}/collections")
        return response.json().get("collections", [])
    except:
        return []

def delete_collection(collection_name):
    response = requests.delete(f"{API_BASE_URL}/collections/{collection_name}")
    return response.json()

st.title("📚 RAG System - 문서 기반 Q&A 시스템")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("📋 컬렉션 관리")
    
    # 컬렉션 선택
    collections = get_collections()
    if collections:
        selected_collection = st.selectbox(
            "컬렉션 선택",
            collections,
            index=0
        )
    else:
        selected_collection = "default"
        st.info("아직 생성된 컬렉션이 없습니다.")
    
    st.markdown("---")
    
    # 컬렉션 삭제
    st.subheader("🗑️ 컬렉션 삭제")
    if collections:
        collection_to_delete = st.selectbox(
            "삭제할 컬렉션",
            collections,
            key="delete_collection"
        )
        if st.button("컬렉션 삭제", type="secondary"):
            result = delete_collection(collection_to_delete)
            st.success(f"컬렉션 '{collection_to_delete}' 삭제 완료!")
            st.rerun()

# 메인 영역
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📁 문서 업로드")
    
    # 컬렉션 이름 입력
    collection_name = st.text_input(
        "컬렉션 이름",
        value=selected_collection,
        help="문서를 저장할 컬렉션 이름을 입력하세요. 새로운 이름을 입력하면 새 컬렉션이 생성됩니다."
    )
    
    # 파일 업로드
    uploaded_file = st.file_uploader(
        "파일 선택",
        type=['pdf', 'docx', 'txt'],
        help="PDF, DOCX, TXT 파일을 업로드할 수 있습니다."
    )
    
    if uploaded_file and st.button("📤 업로드", type="primary"):
        with st.spinner("파일을 처리하고 있습니다..."):
            try:
                result = upload_file(uploaded_file, collection_name)
                st.success(f"✅ 업로드 완료!")
                st.json(result)
            except Exception as e:
                st.error(f"❌ 업로드 실패: {str(e)}")

with col2:
    st.header("💬 질문하기")
    
    # 질문 입력
    question = st.text_area(
        "질문을 입력하세요",
        placeholder="업로드한 문서에 대해 궁금한 것을 질문해보세요...",
        height=100
    )
    
    # 사용할 컬렉션 선택
    target_collection = st.selectbox(
        "질문할 컬렉션",
        collections if collections else ["default"],
        help="질문을 할 문서 컬렉션을 선택하세요."
    )
    
    if question and st.button("🔍 질문하기", type="primary"):
        with st.spinner("답변을 생성하고 있습니다..."):
            try:
                result = chat_with_rag(question, target_collection)
                
                st.markdown("### 📝 답변")
                st.write(result["answer"])
                
                col_conf, col_sources = st.columns([1, 1])
                
                with col_conf:
                    confidence = result.get("confidence", 0.0)
                    st.metric("신뢰도", f"{confidence:.2%}")
                
                with col_sources:
                    sources = result.get("sources", [])
                    if sources:
                        st.markdown("**참조 문서:**")
                        for source in sources:
                            st.write(f"• {source}")
                    else:
                        st.write("참조 문서 없음")
                        
            except Exception as e:
                st.error(f"❌ 답변 생성 실패: {str(e)}")

# 하단 정보
st.markdown("---")
col_info1, col_info2, col_info3 = st.columns([1, 1, 1])

with col_info1:
    st.info("💡 **팁:** PDF, DOCX, TXT 파일을 업로드할 수 있습니다.")

with col_info2:
    st.info("🔧 **설정:** 컬렉션별로 문서를 분류하여 관리할 수 있습니다.")

with col_info3:
    st.info("📊 **성능:** 답변 신뢰도를 참고하여 결과를 판단하세요.")

# 채팅 히스토리 (세션 상태 사용)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.session_state.chat_history:
    st.markdown("---")
    st.header("📜 대화 기록")
    
    for i, (q, a) in enumerate(st.session_state.chat_history):
        with st.expander(f"질문 {i+1}: {q[:50]}..."):
            st.write(f"**질문:** {q}")
            st.write(f"**답변:** {a}")

# 채팅 기록 저장
if 'last_question' in locals() and 'last_answer' in locals():
    st.session_state.chat_history.append((question, result["answer"]))

# 스타일링
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)