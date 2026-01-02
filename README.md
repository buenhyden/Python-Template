# Python Template

**FastAPI**, **uv**, **Docker**를 기반으로 한 강력하고 현대적인 프로덕션 레벨의 Python 프로젝트 템플릿입니다.

## 🚀 주요 기능 (Features)

- **Modern Python**: **Python 3.13** 최신 버전을 기반으로 구축되었습니다.
- **Fast Package Management**: **[uv](https://github.com/astral-sh/uv)**를 사용하여 의존성을 매우 빠르게 관리하고 해결합니다.
- **Dockerized**: 개발, 테스트, 배포 환경에 최적화된 멀티 스테이지 `Dockerfile`을 제공합니다.
- **Event Streaming**: **Kafka**가 **KRaft 모드**(Zookeeper 제거)로 설정되어 있어 가볍고 효율적인 이벤트 스트리밍환경을 제공합니다.
- **High Code Quality**: **Ruff** (린팅/포맷팅), **Mypy** (Strict 타입 검사), **Pre-commit** 뿐만 아니라 **Interrogate** (문서화 커버리지)를 도입하여 최상의 코드 품질을 유지합니다.
- **Databases**: **PostgreSQL 17** 및 **Redis 7**이 즉시 사용 가능한 상태로 설정되어 있습니다.
- **Security Check**: `detect-secrets`와 `pip-audit`을 통해 비밀 정보 노출과 패키지 취약점을 사전에 방지합니다.

## 📂 프로젝트 구조 (Project Structure)

```bash
.
├── .agent/               # MCP Agent 규칙 및 워크플로우
├── .cursor/              # Cursor IDE 전용 규칙
├── .github/              # GitHub Actions 워크플로우 및 템플릿
├── app/                  # 애플리케이션 소스 코드 (Template)
├── deploy/               # Kustomize 배포 설정
│   ├── base/             # 기본 리소스 정의
│   └── overlays/         # 환경별(dev, prod) 오버레이
├── docs/                 # 프로젝트 문서
│   ├── development.md    # 개발 환경 및 도구 설정
│   ├── testing.md        # 테스트 전략 및 실행
│   ├── docker.md         # Docker 멀티 스테이지 빌드
│   ├── ci-cd.md          # GitHub Actions CI/CD
│   └── configuration.md  # 전체 설정 요약
├── logs/                 # 애플리케이션 로그 저장소
├── tests/                # 테스트 코드
│   ├── unit/             # 단위 테스트
│   └── load/             # 부하 테스트
├── Dockerfile            # 멀티 스테이지 Docker 빌드 파일
├── docker-compose.test.yml # 테스트 및 CI용 Docker Compose 설정
├── pyproject.toml        # 프로젝트 설정 및 의존성 관리 (uv)
├── .pre-commit-config.yaml # Git Hook 설정
├── .gitmessage           # Git 커밋 메시지 템플릿
└── .secrets.baseline     # detect-secrets 베이스라인 파일
```

## 🛠️ 기술 스택 (Tech Stack)

- **Language**: Python 3.13
- **Package Manager**: [uv](https://docs.astral.sh/uv/)
- **Web Framework**: FastAPI (권장)
- **Containerization**: Docker
- **Infrastructure**:
    - **PostgreSQL 17** (Database)
    - **Redis 7** (Cache/Broker)
    - **Kafka 7.5.0** (Event Streaming, KRaft Mode)
- **Code Quality & Testing**:
    - **Ruff**: Linting & Formatting (25개 린트 규칙)
    - **Mypy**: Static Type Checking (Strict Mode)
    - **Interrogate**: Documentation Coverage (90% 기준)
    - **Pytest**: Testing Framework + HTML Reports
    - **Pytest 플러그인**: asyncio, cov, html, mock, xdist
    - **Commitizen**: Conventional Commits & Versioning
- **Security**: Detect Secrets, Pip Audit

## 📋 사전 요구사항 (Prerequisites)

- **Python** 3.13 이상
- **Docker** 및 **Docker Compose**
- **uv** (설치 방법: `curl -LsSf https://astral.sh/uv/install.sh | sh`)

## ⚡ 시작하기 (Getting Started)

### 1. 설치 (Installation)

저장소를 클론하고 `uv`를 사용하여 의존성을 설치합니다.

```bash
# 개발 의존성을 포함하여 모든 패키지 설치
uv sync
```

### 2. Pre-commit 설정 (Recommended)

커밋할 때마다 코드 품질을 자동으로 검사하도록 Git Hook을 설치합니다.
이 프로젝트는 엄격한 규칙(문서화, 복잡도, 타입 등)을 적용합니다.

```bash
uv run pre-commit install
```

### 3. 로컬 실행 (Running Locally)

`uv`를 통해 애플리케이션을 로컬 개발 모드로 실행할 수 있습니다.

```bash
# Reload 모드로 실행
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Docker로 실행 (Running with Docker)

이 프로젝트는 효율적인 빌드를 위해 멀티 스테이지 `Dockerfile`을 사용합니다.

**개발 모드 (Development):**
```bash
docker build --target dev -t my-app:dev .
docker run -p 8000:8000 -v $(pwd)/app:/app/app my-app:dev
```

**배포용 빌드 (Production):**
```bash
docker build --target release -t my-app:release .
docker run -p 8000:8000 my-app:release
```

## 📚 문서 (Documentation)

프로젝트 설정 및 개발 가이드는 다음 문서를 참조하세요:

- **[UV 완전 가이드](docs/uv-guide.md)** - uv 패키지 관리자 모든 기능 (기본, 고급, 워크스페이스, 빌드/배포)
- **[개발 환경](docs/development.md)** - 개발 도구, Pre-commit Hooks (14개)
- **[테스트 가이드](docs/testing.md)** - Pytest 설정, Docker 테스트 환경
- **[Docker 가이드](docs/docker.md)** - 6단계 멀티 스테이지 빌드
- **[CI/CD 파이프라인](docs/ci-cd.md)** - GitHub Actions 워크플로우
- **[기여 가이드](docs/contributing.md)** - 워크플로우, 커밋 규칙, 코드 품질 기준
- **[Pre-commit 가이드](docs/pre-commit.md)** - 14개 훅 상세 설정 및 문제 해결
- **[설정 요약](docs/configuration.md)** - 전체 프로젝트 설정 한눈에 보기
- **[UV 완전 가이드](docs/uv-guide.md)** - uv 패키지 관리자 모든 기능

## 📘 UV 패키지 관리자

이 프로젝트는 `uv`를 사용하여 Python 패키지 및 의존성을 관리합니다.

**주요 특징:**
- **극도로 빠름**: pip 대비 10-100배 빠른 성능
- **통합 관리**: 패키지, 의존성, Python 버전, 가상환경 모두 관리
- **재현 가능**: `uv.lock` 파일로 정확한 의존성 고정
- **현대적**: `pyproject.toml` 중심의 프로젝트 관리

**빠른 시작:**
```bash
# 의존성 설치
uv sync

# 패키지 추가
uv add package-name

# 개발 의존성 추가
uv add --dev pytest ruff

# 스크립트 실행 (가상환경 자동 활성화)
uv run pytest
uv run uvicorn app.main:app --reload
```

**상세 가이드:** [UV 완전 가이드](docs/uv-guide.md) - 고급 기능, 워크스페이스, 빌드/배포, 설정 등 모든 내용

## 🔐 보안 및 비밀 관리 (Secrets Management)

이 프로젝트는 `detect-secrets`를 사용하여 비밀 정보 노출을 방지합니다. 자세한 설정과 사용법은 **[Pre-commit 가이드](docs/pre-commit.md)**를 참조하세요.


## 📝 Git 커밋 컨벤션 (Commit Convention)

이 프로젝트는 [Conventional Commits](https://www.conventionalcommits.org/) 형식을 따릅니다. 상세한 규칙은 **[기여 가이드](docs/contributing.md)**를 확인해주세요.

```text
<type>: <subject>
```


## 🧪 테스트 (Testing)

엄격한 품질 관리를 위해 테스트 코드 작성은 필수입니다. 자세한 내용은 **[테스트 가이드](docs/testing.md)**를 참조하세요.

```bash
# Unit Test 실행
uv run pytest

# Docker Compose 통합 테스트
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```


## 📋 코드 품질 및 기여 (Quality & Contribution)

이 프로젝트는 높은 코드 품질을 유지하기 위해 엄격한 기준을 적용합니다. 자세한 내용은 **[기여 가이드](docs/contributing.md)**를 참조하세요.

### 주요 도구
- **Ruff**: Linting & Formatting (라인 길이 120, Google Style Docstring)
- **Mypy**: Strict Type Checking
- **Interrogate**: 문서화 커버리지 90% 이상
- **Pre-commit**: 커밋 전 14개 항목 자동 검사 (상세 내용: **[Pre-commit 가이드](docs/pre-commit.md)**)

### 검사 실행하기
```bash
# 전체 품질 검사
uv run pre-commit run --all-files

# 테스트 및 커버리지
uv run pytest --cov
```

## 🤝 기여 방법 (How to Contribute)

1. 저장소 Fork 및 Clone
2. 브랜치 생성 (`feat/function-name`)
3. 코드 작성 및 테스트
4. 커밋 (Conventional Commits 준수)
   - `uv run cz commit` 사용 권장
5. Pull Request 생성

> **자세한 기여 방법과 커밋 규칙은 [기여 가이드](docs/contributing.md)를 확인해주세요.**

## � Docker 빌드 (Docker Build)

프로젝트는 6단계 멀티 스테이지 빌드를 사용합니다. 자세한 내용은 **[Docker 가이드](docs/docker.md)**를 참조하세요.

```bash
# 로컬 개발용 빌드 및 실행
docker build --target dev -t my-app:dev .
```
