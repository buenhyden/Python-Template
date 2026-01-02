# Docker 가이드 (Docker Guide)

이 문서는 프로젝트의 Docker 설정과 멀티 스테이지 빌드에 대해 설명합니다.

## Dockerfile 개요

프로젝트는 **6개의 멀티 스테이지 빌드**를 사용하여 다양한 용도에 최적화된 이미지를 제공합니다.

### 스테이지 구조

```
base (Python 3.13 + uv)
  ├─> prod-deps (프로덕션 의존성)
  │     └─> release (최종 배포용)
  └─> dev-deps (개발 의존성)
        ├─> test (CI/CD 테스트용)
        └─> dev (로컬 개발용)
```

## Stage 1: base

### 목적
모든 스테이지의 공통 기반 이미지

### 기반 이미지
```dockerfile
FROM python:3.13-slim as base
```

### 주요 구성

#### uv 설치
```dockerfile
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
```

#### 환경 변수
```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    TZ=Asia/Seoul
```

| 변수 | 설명 |
|------|------|
| `PYTHONDONTWRITEBYTECODE=1` | .pyc 파일 생성 방지 |
| `PYTHONUNBUFFERED=1` | 버퍼링 비활성화 (로그 즉시 출력) |
| `UV_COMPILE_BYTECODE=1` | uv가 bytecode 컴파일 |
| `UV_LINK_MODE=copy` | 심볼릭 링크 대신 복사 |
| `TZ=Asia/Seoul` | 타임존 설정 |

#### 시스템 의존성
```dockerfile
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
```

## Stage 2: prod-deps

### 목적
프로덕션 의존성만 설치 (개발 도구 제외)

### 빌드 과정

```dockerfile
FROM base AS prod-deps

COPY ./pyproject.toml ./uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev
```

### 주요 옵션

| 옵션 | 설명 |
|------|------|
| `--frozen` | uv.lock과 불일치 시 에러 (재현성 보장) |
| `--no-install-project` | 프로젝트 자체는 설치하지 않음 |
| `--no-dev` | 개발 의존성 제외 |

### 캐싱
```dockerfile
--mount=type=cache,target=/root/.cache/uv
```
uv 캐시를 마운트하여 빌드 속도 향상

## Stage 3: dev-deps

### 목적
개발 의존성 포함 전체 설치

### 빌드 과정

```dockerfile
FROM prod-deps AS dev-deps

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project
```

- pytest, ruff, mypy
- pre-commit
- commitizen, detect-secrets
- 등 14개 개발 도구

## Stage 4: test (CI/CD용)

### 목적
CI/CD 파이프라인에서 테스트 실행

### 빌드 과정

```dockerfile
FROM dev-deps AS test

WORKDIR /app
RUN mkdir /app/logs

COPY ./app ./app
COPY ./tests ./tests
COPY .pre-commit-config.yaml .
COPY pyproject.toml .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

CMD ["uv", "run", "pytest"]
```

### 특징
- 소스 및 테스트 코드 포함
- Pre-commit 설정 포함 (품질 검사용)
- 기본 CMD로 pytest 실행

### 사용

```bash
# 빌드
docker build --target test -t myapp:test .

# 실행
docker run --rm myapp:test

# 또는 Docker Compose 사용
docker compose -f docker-compose.test.yml run --rm test
```

## Stage 5: release (프로덕션 배포용)

### 목적
최종 배포를 위한 최소 크기 이미지

### 빌드 과정

```dockerfile
FROM python:3.13-slim AS release

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Seoul

# 런타임 라이브러리만 설치
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 비-루트 유저 생성
RUN useradd -m -s /bin/bash appuser
WORKDIR /app

# prod-deps에서 가상환경만 복사
COPY --from=prod-deps --chown=appuser:appuser /app/.venv /app/.venv

# 소스 코드 복사
COPY --chown=appuser:appuser ./app ./app

USER appuser
```

### 보안 특징

1. **비-루트 사용자 실행**
   ```dockerfile
   RUN useradd -m -s /bin/bash appuser
   USER appuser
   ```

2. **최소 의존성**
   - 개발 도구 없음
   - 런타임 라이브러리만 설치

3. **파일 권한**
   ```dockerfile
   COPY --chown=appuser:appuser
   ```

### 사용

```bash
# 빌드
docker build --target release -t myapp:release .

# 실행
docker run -p 8000:8000 myapp:release \
  uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Stage 6: dev (로컬 개발용)

### 목적
로컬 개발 환경 (편의 도구 포함)

### 빌드 과정

```dockerfile
FROM dev-deps AS dev

# 개발 도구 설치
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ca-certificates \
    default-libmysqlclient-dev \
    git \
    wget \
    procps \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app/scripts/

# 프로젝트 파일 복사
COPY .github/ ./.github/
COPY deploy/ ./deploy/
COPY ./README.md ./README.md
COPY ./.gitignore ./
COPY ./.dockerignore ./
COPY ./.pre-commit-config.yaml .
COPY ./.gitmessage .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

COPY ./app ./app
```

### 포함된 도구
- `git` - 버전 관리
- `vim` - 텍스트 편집기
- `wget`, `curl` - 다운로드
- `procps` - 프로세스 관리 (ps, top 등)

### 사용

```bash
# 빌드
docker build --target dev -t myapp:dev .

# 실행 (볼륨 마운트)
docker run -it --rm \
  -v $(pwd)/app:/app/app \
  -p 8000:8000 \
  myapp:dev \
  uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**reload 옵션으로 코드 변경 시 자동 재시작**

## 스테이지별 사용 시나리오

| 스테이지 | 용도 | 크기 | 포함 내용 |
|----------|------|------|-----------|
| `base` | 공통 기반 | 중간 | Python + uv + 시스템 라이브러리 |
| `prod-deps` | 의존성 빌드 | 중간 | 프로덕션 의존성만 |
| `dev-deps` | 의존성 빌드 | 큰 | 모든 의존성 |
| `test` | CI/CD 테스트 | 큰 | 소스 + 테스트 + 도구 |
| `release` | 프로덕션 배포 | 작음 | 소스 + 런타임만 |
| `dev` | 로컬 개발 | 매우 큼 | 모든 것 + 개발 도구 |

## Docker Compose 설정

### docker-compose.test.yml

테스트 환경 구성

#### 서비스 구조

```yaml
services:
  run:         # 개발 실행용
  test:        # 테스트 실행용
  postgres:    # 데이터베이스
  redis:       # 캐시/브로커
  kafka:       # 이벤트 스트리밍
```

#### test 서비스

```yaml
test:
  build:
    context: .
    dockerfile: Dockerfile
    target: test
  environment:
    # ... 45개 환경 변수
  depends_on:
    postgres:
      condition: service_healthy
    redis:
      condition: service_started
    kafka:
      condition: service_started
```

**의존성 관리:**
- PostgreSQL health check 대기
- Redis, Kafka 시작 대기

#### PostgreSQL 서비스

```yaml
postgres:
  image: postgres:17-bookworm
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: password
    POSTGRES_DB: app_db
  ports:
    - "5432:5432"
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 5s
    timeout: 5s
    retries: 5
```

#### Redis 서비스

```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
```

#### Kafka 서비스 (KRaft 모드)

```yaml
kafka:
  image: confluentinc/cp-kafka:7.5.0
  ports:
    - "9092:9092"
  environment:
    KAFKA_NODE_ID: 1
    KAFKA_PROCESS_ROLES: broker,controller
    KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:29093
    # ... KRaft 설정
```

**KRaft 모드:**
- Zookeeper 불필요
- 더 간단한 아키텍처
- 빠른 시작 시간

### 실행

```bash
# 모든 서비스 시작
docker compose -f docker-compose.test.yml up

# 테스트만 실행
docker compose -f docker-compose.test.yml run --rm test

# 빌드 포함
docker compose -f docker-compose.test.yml up --build

# 정리
docker compose -f docker-compose.test.yml down -v
```

## 빌드 최적화

### 1. 레이어 캐싱

의존성 파일을 먼저 복사하여 캐싱 활용:

```dockerfile
# 의존성 파일만 먼저 복사
COPY ./pyproject.toml ./uv.lock ./

# 의존성 설치 (변경 시에만 재빌드)
RUN uv sync --frozen

# 소스 코드는 나중에 복사 (자주 변경됨)
COPY ./app ./app
```

### 2. BuildKit 캐시 마운트

```dockerfile
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen
```

빌드 간 캐시 공유로 속도 향상

### 3. 멀티 스테이지 빌드

- base 스테이지 재사용
- 최종 이미지 크기 최소화
- 빌드 도구 제외

## 이미지 크기 비교

| 스테이지 | 예상 크기 | 설명 |
|----------|-----------|------|
| `base` | ~400MB | Python + 기본 도구 |
| `prod-deps` | ~500MB | + 프로덕션 의존성 |
| `dev-deps` | ~700MB | + 개발 의존성 |
| `test` | ~800MB | + 소스 + 테스트 |
| `release` | ~400MB | 최소화된 프로덕션 |
| `dev` | ~900MB | + 개발 도구 |

## 보안 Best Practices

### 1. 비-루트 사용자

```dockerfile
RUN useradd -m -s /bin/bash appuser
USER appuser
```

### 2. 최소 권한 원칙

프로덕션에 불필요한 도구 제외

### 3. 이미지 스캔

```bash
# Trivy로 취약점 스캔
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image myapp:release
```

### 4. 비밀 정보 제외

`.dockerignore` 사용:
```
.env
.secrets
*.key
*.pem
```

## 로컬 개발 워크플로우

### 1. 개발 이미지 빌드

```bash
docker build --target dev -t myapp:dev .
```

### 2. 볼륨 마운트로 실행

```bash
docker run -it --rm \
  -v $(pwd)/app:/app/app \
  -v $(pwd)/tests:/app/tests \
  -p 8000:8000 \
  -e DEBUG=True \
  myapp:dev \
  uv run uvicorn app.main:app --reload
```

### 3. 컨테이너 내부 접근

```bash
docker run -it --rm myapp:dev bash
```

## 프로덕션 배포

### 1. Release 이미지 빌드

```bash
docker build --target release -t myapp:1.0.0 .
docker tag myapp:1.0.0 myapp:latest
```

### 2. 레지스트리에 푸시

```bash
docker tag myapp:1.0.0 ghcr.io/username/myapp:1.0.0
docker push ghcr.io/username/myapp:1.0.0
```

### 3. 실행

```bash
docker run -d \
  --name myapp \
  -p 8000:8000 \
  -e SECRET_KEY=$SECRET_KEY \
  -e DB_URL=$DB_URL \
  myapp:1.0.0 \
  uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 트러블슈팅

### 빌드 실패

```bash
# 캐시 없이 빌드
docker build --no-cache --target release -t myapp:release .

# BuildKit 활성화
export DOCKER_BUILDKIT=1
```

### 이미지 크기 분석

```bash
# 레이어 확인
docker history myapp:release

# dive로 상세 분석
dive myapp:release
```

### 로그 확인

```bash
# 컨테이너 로그
docker logs <container-id>

# 실시간 로그
docker logs -f <container-id>
```
