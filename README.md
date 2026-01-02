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
    - **Ruff**: Linting & Formatting (Strict Rules applied)
    - **Mypy**: Static Type Checking (Strict Mode)
    - **Interrogate**: Documentation Coverage Check (Fail under 90%)
    - **Pytest**: Testing Framework
    - **Pytest-mock**: Mocking library for tests
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

## 🔐 보안 및 비밀 관리 (Secrets Management)

이 프로젝트는 `detect-secrets`를 사용하여 소스 코드에 비밀 정보(API Key, Password 등)가 포함되는 것을 방지합니다.

**비밀 정보 스캔 및 베이스라인 업데이트:**

새로운 비밀 정보가 감지되었을 때, 의도된 것이라면 베이스라인을 업데이트해야 합니다.

```bash
# 전체 파일 스캔 및 베이스라인 갱신
uv run detect-secrets scan > .secrets.baseline

# 베이스라인 검사 (CI에서 수행됨)
uv run detect-secrets-hook --baseline .secrets.baseline $(git ls-files)
```

## 📝 Git 커밋 컨벤션 (Commit Convention)

`.gitmessage` 파일에 정의된 규칙을 따릅니다. 커밋 메시지는 다음과 같은 형식을 권장합니다:

```text
<type> : <subject>

<body (optional)>

<footer> (optional)
```

- **type**: `feat`, `fix`, `refactor`, `style`, `docs`, `test`, `chore`, `build`, `ci`, `release`
- **subject**: 50자 이내, 명확한 변경 사항 요약, 마침표(.) 금지

## 🧪 테스트 (Testing)

엄격한 품질 관리를 위해 테스트 코드 작성은 필수입니다.

**Unit Test 실행:**

```bash
uv run pytest
```
*Tip: `interrogate`가 `docs`와 `tests`를 제외한 모든 모듈의 문서화율 90% 이상을 요구합니다.*
*Tip: `pytest-mock`을 사용하여 외부 의존성을 쉽게 모킹할 수 있습니다.*

**Docker Compose를 이용한 통합 테스트:**

격리된 환경(DB, Redis, Kafka 포함)에서 전체 테스트를 수행합니다.

```bash
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

### 테스트 환경 변수 (Test Environment)

`docker-compose.test.yml`은 테스트를 위해 다음 서비스들을 자동으로 구성합니다:

| 서비스 | 설정 | 비고 |
|--------|------|------|
| **PostgreSQL** | User: `postgres`, DB: `app_db` | 데이터베이스 |
| **Redis** | Port: `6379` | 캐시 및 메시지 브로커 |
| **Kafka** | KRaft Mode, Port: `9092` | Zookeeper 없이 동작 |

## 📦 Docker Stages 상세 (Docker Stages)

1.  **base**: OS 기본 패키지 및 `uv` 설치.
2.  **prod-deps**: 프로덕션용 Python 의존성 설치.
3.  **dev-deps**: 개발용 의존성 설치.
4.  **test**: CI/CD 파이프라인에서 테스트 수행용.
5.  **release**: 최종 배포용 경량 이미지 (Non-root 사용자 실행).
6.  **dev**: 로컬 개발용 (Git, Vim 등 도구 포함).
