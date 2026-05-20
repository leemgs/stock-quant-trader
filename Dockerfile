FROM python:3.9-slim

WORKDIR /app

# 시스템 의존성 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 파이썬 의존성 패키지 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# src/ 폴더의 모듈을 인식할 수 있도록 PYTHONPATH 설정
ENV PYTHONPATH=/app/src:$PYTHONPATH
