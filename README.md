# LLM + RAG 시스템

문서 업로드 후 해당 문서를 참조하여 질문에 답변하는 RAG(Retrieval-Augmented Generation) 시스템입니다.

## 🚀 주요 기능

- **문서 업로드**: PDF, DOCX, TXT 파일 지원
- **문서 처리**: 자동 텍스트 추출 및 청킹
- **벡터 검색**: ChromaDB를 활용한 시맨틱 검색
- **RAG 답변**: OpenAI GPT를 활용한 문서 기반 답변 생성
- **컬렉션 관리**: 문서를 카테고리별로 분류 관리
- **웹 UI**: Streamlit 기반의 직관적인 사용자 인터페이스

## 📋 시스템 구조

```
rag-system/
├── backend/
│   ├── app/
│   │   └── main.py              # FastAPI 메인 애플리케이션
│   └── services/
│       ├── document_processor.py # 문서 처리 및 청킹
│       ├── vector_store.py       # ChromaDB 벡터 저장소
│       └── rag_service.py        # RAG 답변 생성 서비스
├── frontend/
│   └── app.py                   # Streamlit 웹 인터페이스
├── documents/                   # 업로드된 문서 저장
├── vector_db/                   # ChromaDB 데이터
├── requirements.txt             # Python 의존성
└── .env.example                # 환경변수 템플릿
```

## 🛠️ 설치 및 설정

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env.example`을 복사하여 `.env` 파일을 생성하고 필요한 값들을 설정하세요:

```bash
cp .env.example .env
```

`.env` 파일에서 다음 값을 설정하세요:
- `OPENAI_API_KEY`: OpenAI API 키

### 3. 디렉토리 생성

```bash
mkdir -p documents vector_db
```

## 🚀 실행 방법

### 1. 백엔드 서버 실행

```bash
python run_backend.py
```

또는

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 프론트엔드 실행

새 터미널에서:

```bash
python run_frontend.py
```

또는

```bash
streamlit run frontend/app.py
```

### 3. 웹 브라우저에서 접속

- 프론트엔드: http://localhost:8501
- 백엔드 API 문서: http://localhost:8000/docs

## 📖 사용 방법

### 1. 문서 업로드
1. 웹 인터페이스에서 "문서 업로드" 섹션으로 이동
2. 컬렉션 이름 입력 (기본값: default)
3. PDF, DOCX, 또는 TXT 파일 선택
4. "업로드" 버튼 클릭

### 2. 질문하기
1. "질문하기" 섹션에서 질문 입력
2. 질문할 컬렉션 선택
3. "질문하기" 버튼 클릭
4. AI가 업로드된 문서를 기반으로 답변 생성

### 3. 컬렉션 관리
- 사이드바에서 컬렉션 선택 및 삭제 가능
- 여러 컬렉션을 만들어 문서를 카테고리별로 분류

## 🔧 API 엔드포인트

### POST /upload
문서를 업로드하고 벡터 DB에 저장

### POST /chat
질문에 대한 RAG 답변 생성

### GET /collections
모든 컬렉션 목록 조회

### DELETE /collections/{collection_name}
특정 컬렉션 삭제

## ⚙️ 설정 옵션

### 문서 처리 설정
- `chunk_size`: 텍스트 청크 크기 (기본값: 1000)
- `chunk_overlap`: 청크 간 중복 크기 (기본값: 200)

### 검색 설정
- `n_results`: 검색할 유사 문서 수 (기본값: 5)
- `similarity_threshold`: 유사도 임계값

### LLM 설정
- `model`: 사용할 GPT 모델 (기본값: gpt-3.5-turbo)
- `temperature`: 답변 생성 창의성 (기본값: 0.3)
- `max_tokens`: 최대 토큰 수 (기본값: 1500)

## 🔄 로컬 LLM 사용

OpenAI 대신 로컬 LLM(Ollama)을 사용하려면:

1. Ollama 설치: https://ollama.ai
2. 모델 다운로드: `ollama pull llama2`
3. `rag_service.py`에서 `LocalRAGService` 사용

## 🐳 Docker 배포

```dockerfile
# Dockerfile 예시
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000 8501

CMD ["python", "run_backend.py"]
```

## 📝 주의사항

1. **API 키 보안**: `.env` 파일을 버전 관리에 포함하지 마세요
2. **파일 크기 제한**: 대용량 파일은 처리 시간이 오래 걸릴 수 있습니다
3. **메모리 사용량**: 많은 문서를 업로드하면 메모리 사용량이 증가합니다

## 🤝 기여

버그 리포트나 기능 제안은 GitHub Issues를 통해 제출해주세요.

## 📄 라이선스

MIT License