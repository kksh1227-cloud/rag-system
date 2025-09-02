# 🚀 RAG 시스템 배포 가이드

## 배포 옵션

### 1. 백엔드 배포 (Railway/Render)

#### Railway 배포
1. [Railway](https://railway.app) 회원가입/로그인
2. "New Project" → "Deploy from GitHub repo" 선택
3. 이 저장소 선택
4. 환경변수 설정:
   - `OPENAI_API_KEY`: OpenAI API 키
   - `PORT`: 8000
5. 자동 배포 완료 → API URL 확인

#### Render 배포
1. [Render](https://render.com) 회원가입/로그인
2. "New" → "Web Service" 선택
3. GitHub 저장소 연결
4. 설정:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run_backend.py`
5. 환경변수 설정:
   - `OPENAI_API_KEY`: OpenAI API 키
6. 배포 완료 → API URL 확인

### 2. 프론트엔드 배포 (Streamlit Cloud)

1. [Streamlit Cloud](https://share.streamlit.io) 로그인
2. "New app" 클릭
3. 저장소 정보 입력:
   - Repository: `your-username/rag-system`
   - Branch: `main` 
   - Main file path: `streamlit_app.py`
4. "Deploy!" 클릭
5. 앱 URL 확인

### 3. 통합 배포

프론트엔드의 `API_BASE_URL`을 백엔드 배포 URL로 수정:

```python
# frontend/app.py 수정
API_BASE_URL = "https://your-backend-url.railway.app"  # 또는 Render URL
```

## 필요한 환경변수

### 백엔드
- `OPENAI_API_KEY`: OpenAI API 키 (필수)
- `PORT`: 포트 번호 (기본값: 8000)
- `DEBUG`: 디버그 모드 (기본값: False)

### 프론트엔드 (Streamlit Cloud Secrets)
```toml
# secrets.toml (Streamlit Cloud에서 설정)
OPENAI_API_KEY = "your_openai_api_key"
BACKEND_URL = "https://your-backend-url.railway.app"
```

## 배포 후 확인사항

1. **백엔드 API 테스트**: `https://your-backend-url/docs`
2. **프론트엔드 접속**: Streamlit Cloud URL
3. **파일 업로드 테스트**
4. **질의응답 테스트**

## 비용 정보

- **Railway**: 월 $5 (1GB RAM, 1 vCPU)
- **Render**: 무료 플랜 (제한적), Pro $7/월
- **Streamlit Cloud**: 무료 (공개 앱)

## 보안 주의사항

1. **API 키 노출 방지**: .env 파일을 GitHub에 업로드하지 마세요
2. **CORS 설정**: 프로덕션에서는 특정 도메인만 허용
3. **파일 업로드 제한**: 악의적 파일 업로드 방지

## 모니터링

- **로그 확인**: Railway/Render 대시보드에서 로그 모니터링
- **성능 모니터링**: 응답 시간, 메모리 사용량 확인
- **오류 추적**: 오류 로그 정기적 확인