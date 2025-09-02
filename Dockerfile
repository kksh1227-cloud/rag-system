FROM python:3.9-slim

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 필요한 디렉토리 생성
RUN mkdir -p documents vector_db

# 백엔드 경로를 PYTHONPATH에 추가
ENV PYTHONPATH="/app/backend:$PYTHONPATH"

# 포트 노출
EXPOSE 8000

# 백엔드 서버 실행
CMD ["python", "run_backend.py"]