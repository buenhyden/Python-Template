# === Stage 1: "base" (공통 기반) ===
FROM python:3.12-slim as base
LABEL version="0.1" creator="chochyjj@gmail.com" description="Python 3.12"
# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    TZ=Asia/Seoul

# 1. Timezone 설정
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# 2. 시스템 의존성 설치 (빌드 및 런타임 공통)
# gcc, libmysqlclient-dev 등은 Python 패키지 컴파일(빌드)에 필수입니다.
# 런타임 시에는 가벼운 라이브러리만 필요하더라도, 빌드 단계(base)에서는 dev 패키지가 필요합니다.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 3. Poetry 설치
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# ==========================================
# Stage 2: Production Dependencies (프로덕션 의존성 빌드)
# ==========================================
FROM base AS prod-deps

# 의존성 파일 복사 (캐싱 활용)
COPY ./pyproject.toml ./

# 프로덕션 의존성만 설치 (.venv 생성)
RUN poetry install --no-root --only main

# ==========================================
# Stage 3: Development Dependencies (개발 의존성 빌드)
# ==========================================
FROM prod-deps AS dev-deps

# 개발 의존성 포함 전체 설치
RUN poetry install --no-root

# ==========================================
# Stage 4: Release (최종 배포용 이미지)
# ==========================================
FROM python:3.12-slim AS release

# 런타임 환경 변수
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Seoul

# 1. 런타임 시스템 라이브러리 및 Timezone 설정
# (빌드 도구는 제외하고 실행에 필요한 라이브러리만 설치하여 경량화)
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. 보안을 위한 비-루트 유저 생성
RUN useradd -m -s /bin/bash appuser
WORKDIR /app

# 3. prod-deps 단계에서 생성된 가상환경(.venv)만 복사
COPY --from=prod-deps --chown=appuser:appuser /app/.venv /app/.venv

# 4. 소스 코드 복사
COPY --chown=appuser:appuser ./src ./src

# 5. 유저 전환 및 실행
USER appuser
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ==========================================
# Stage 5: Test (테스트 실행용 이미지)
# ==========================================
FROM dev-deps AS test

# 가상환경 경로 설정
ENV PATH="/app/.venv/bin:$PATH"

# 소스 코드 복사
COPY ./src ./src
COPY ./tests ./tests

# 테스트 실행
CMD ["pytest"]

# ==========================================
# Stage 6: Dev (로컬 개발용 이미지)
# ==========================================
FROM dev-deps AS dev

# 개발 편의 도구 설치 (git, vim 등)
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates default-libmysqlclient-dev git wget procps git vim \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir /app/scripts/
COPY .github/ ./.github/
COPY deploy/ ./deploy/
COPY ./README.md ./README.md
COPY ./.gitignore ./
COPY ./.dockerignore ./
COPY ./.pre-commit-config.yaml .
COPY ./.gitmessage .
# COPY ./.ssh /root/.ssh  <-- Removed
# /////////////////////////////////////////////////////////////////
# github SSH key 사용 (제거됨)
# /////////////////////////////////////////////////////////////////
# RUN git config --global core.editor "code --wait"
# RUN git config --global user.email "chochyjj@gmail.com"
# RUN git config --global user.name "Hyunyoun Jo"
# RUN chmod 600 /root/.ssh/id_rsa
# RUN chmod 600 /root/.ssh/id_rsa.pub
# Command to run the application in development mode
# --reload: Enables hot-reloading
# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# 소스 코드 복사 (Docker Compose 볼륨 마운트 사용 시 덮어씌워짐)
COPY ./src ./src

# 개발 모드 실행 (Reload 옵션 활성화)
CMD ["zsh", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
