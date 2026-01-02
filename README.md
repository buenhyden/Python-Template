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
- **[개발 환경](docs/development.md)** - 개발 도구, Pre-commit Hooks (14개), Commitizen 설정
- **[테스트 가이드](docs/testing.md)** - Pytest 설정, Docker 테스트 환경, 커버리지 80% 기준
- **[Docker 가이드](docs/docker.md)** - 6단계 멀티 스테이지 빌드, 컨테이너 최적화
- **[CI/CD 파이프라인](docs/ci-cd.md)** - GitHub Actions 워크플로우, 캐싱 전략
- **[설정 요약](docs/configuration.md)** - 전체 프로젝트 설정 한눈에 보기

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

## 📋 코드 품질 및 기여 가이드 (Code Quality & Contribution)

이 프로젝트는 높은 코드 품질을 유지하기 위해 엄격한 린팅, 타입 체크, 테스트 커버리지 기준을 적용합니다. 모든 기여자는 아래 가이드라인을 따라야 합니다.

### 🔧 코드 품질 도구 (Code Quality Tools)

#### Ruff - Linting & Formatting

Python 코드의 품질을 검사하고 자동으로 포맷팅합니다. 기존 도구 대비 **10-100배 빠른 성능**을 제공합니다.

**주요 설정:**
- 라인 길이: 120자
- 타겟 Python 버전: 3.13
- 문서화 스타일: Google Style
- 복잡도 제한: 10 이하 (McCabe)

**사용 명령어:**
```bash
# 전체 코드 검사
uv run ruff check .

# 자동 수정 가능한 문제 수정
uv run ruff check . --fix

# 코드 포맷팅
uv run ruff format .

# 특정 파일만 검사
uv run ruff check app/main.py
```

**적용된 린트 규칙:**
- `E`, `F`: 기본 에러 및 논리 오류
- `I`: Import 정렬 (isort)
- `N`: 명명 규칙 (PEP 8)
- `D`: 문서화 규칙 (pydocstyle)
- `S`: 보안 검사 (bandit)
- `B`: 설계 문제 (bugbear)
- `C90`: 복잡도 검사 (mccabe)
- `UP`: 최신 문법 사용 (pyupgrade)
- `SIM`: 코드 간소화
- `PERF`: 성능 최적화
- `PL`: Pylint 규칙

#### Mypy - Static Type Checking

정적 타입 검사를 통해 런타임 전에 타입 관련 오류를 발견합니다.

**주요 설정:**
- **Strict Mode** 활성화
- 타입 힌트 없는 함수 호출 금지
- Pydantic 플러그인 사용

**사용 명령어:**
```bash
# 전체 코드 타입 체크
uv run mypy .

# 특정 디렉토리만 체크
uv run mypy app/

# 상세 출력
uv run mypy . --pretty
```

**타입 힌트 예제:**
```python
from typing import Optional

def get_user(user_id: int) -> Optional[dict]:
    """사용자 정보를 조회합니다."""
    # 구현
    pass
```

#### Interrogate - Documentation Coverage

코드 문서화율을 측정하고 강제합니다.

**주요 설정:**
- 최소 문서화율: **90%**
- 제외 디렉토리: `docs`, `tests`
- Google 스타일 docstring 사용

**사용 명령어:**
```bash
# 문서화 커버리지 확인
uv run interrogate -vv app/

# 배지 생성
uv run interrogate -g -vv app/
```

**Docstring 예제:**
```python
def calculate_total(items: list[float], tax_rate: float = 0.1) -> float:
    """
    항목들의 총합을 세금 포함하여 계산합니다.

    Args:
        items: 가격 목록
        tax_rate: 세율 (기본값: 0.1)

    Returns:
        세금을 포함한 총 금액

    Raises:
        ValueError: items가 비어있을 때

    Examples:
        >>> calculate_total([100, 200], 0.1)
        330.0
    """
    if not items:
        raise ValueError("Items cannot be empty")
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

#### Pytest - Testing & Coverage

테스트 프레임워크 및 코드 커버리지 측정

**주요 설정:**
- 최소 커버리지: **80%**
- 비동기 테스트 지원 (pytest-asyncio)
- 병렬 테스트 실행 (pytest-xdist)
- 모킹 지원 (pytest-mock)

**사용 명령어:**
```bash
# 모든 테스트 실행
uv run pytest

# 커버리지 포함 실행
uv run pytest --cov

# 병렬 실행 (4개 프로세스)
uv run pytest -n 4

# 특정 테스트만 실행
uv run pytest tests/unit/test_user.py

# 상세 출력
uv run pytest -vv

# 실패한 테스트만 재실행
uv run pytest --lf
```

### 🔒 보안 검사 (Security Checks)

#### detect-secrets - 비밀 정보 검사

소스 코드에 API 키, 비밀번호 등이 포함되는 것을 방지합니다.

**사용 명령어:**
```bash
# 전체 스캔 및 베이스라인 업데이트
uv run detect-secrets scan > .secrets.baseline

# 베이스라인 검사
uv run detect-secrets-hook --baseline .secrets.baseline $(git ls-files)

# 베이스라인 감사 (대화형)
uv run detect-secrets audit .secrets.baseline
```

#### pip-audit - 패키지 취약점 검사

설치된 패키지의 알려진 보안 취약점을 검사합니다.

**사용 명령어:**
```bash
# 의존성 취약점 검사
uv run pip-audit

# JSON 형식으로 출력
uv run pip-audit --format json
```

### 🪝 Pre-commit Hooks

커밋 전에 자동으로 코드 품질 검사를 수행합니다.

**설치:**
```bash
uv run pre-commit install
```

**포함된 검사 항목:**
1. **파일 검사**: JSON, YAML, TOML 문법 검사
2. **코드 스타일**: 파일 끝 줄바꿈, 공백 제거
3. **YAML 포맷팅**: yamlfmt
4. **맞춤법 검사**: codespell
5. **Ruff**: 린팅 및 포맷팅
6. **Interrogate**: 문서화 커버리지
7. **Mypy**: 타입 체크
8. **detect-secrets**: 비밀 정보 검사
9. **uv lock 검사**: 의존성 동기화 확인

**수동 실행:**
```bash
# 모든 파일에 대해 실행
uv run pre-commit run --all-files

# 특정 훅만 실행
uv run pre-commit run ruff --all-files

# 스테이징된 파일만 검사
uv run pre-commit run
```

**Pre-commit 건너뛰기 (비권장):**
```bash
git commit --no-verify -m "message"
```

### ⚙️ 코드 품질 기준 (Quality Standards)

모든 코드는 다음 기준을 충족해야 합니다:

| 항목 | 기준 | 도구 | 비고 |
|------|------|------|------|
| **문서화율** | ≥ 90% | Interrogate | Google 스타일 docstring |
| **테스트 커버리지** | ≥ 80% | Coverage | `__init__.py` 제외 |
| **복잡도** | ≤ 10 | McCabe (Ruff) | 함수당 순환 복잡도 |
| **타입 체크** | Strict | Mypy | 모든 함수에 타입 힌트 |
| **라인 길이** | ≤ 120 | Ruff | 한 줄 최대 길이 |
| **보안 검사** | 통과 | Bandit (Ruff) | 보안 취약점 없음 |

**품질 기준 미달 시:**
- Pre-commit 훅이 커밋을 차단합니다
- CI/CD 파이프라인에서 빌드가 실패합니다
- Pull Request가 머지되지 않습니다

### 📝 커밋 컨벤션 (Commit Conventions)

이 프로젝트는 [Conventional Commits](https://www.conventionalcommits.org/) 형식을 따릅니다.

**커밋 메시지 형식:**
```
<type> : <subject>

<body (optional)>

<footer (optional)>
```

**타입 (Type) 목록:**

| 타입 | 설명 | 예시 |
|------|------|------|
| `feat` | 새로운 기능 추가 | `feat : 사용자 로그인 기능 추가` |
| `fix` | 버그 수정 | `fix : 로그인 시 세션 만료 오류 수정` |
| `refactor` | 코드 리팩토링 | `refactor : 사용자 서비스 레이어 분리` |
| `style` | 코드 포맷팅, 세미콜론 누락 등 | `style : Ruff 포맷팅 적용` |
| `docs` | 문서 수정 | `docs : README에 설치 가이드 추가` |
| `test` | 테스트 코드 추가/수정 | `test : 사용자 API 단위 테스트 추가` |
| `chore` | 빌드, 패키지 매니저 수정 | `chore : uv 의존성 업데이트` |
| `build` | 빌드 시스템 수정 | `build : Docker 이미지 최적화` |
| `ci` | CI/CD 설정 수정 | `ci : GitHub Actions 워크플로우 추가` |
| `release` | 버전 릴리즈 | `release : v1.0.0` |

**커밋 메시지 작성 규칙:**
- 제목은 50자 이내로 작성
- 제목 끝에 마침표(`.`) 금지
- 제목은 명령문 사용 (과거형 X)
- 본문은 72자마다 줄바꿈
- 본문에서 "무엇을", "왜" 변경했는지 설명

**커밋 템플릿 설정:**
```bash
git config commit.template .gitmessage
```

**좋은 커밋 메시지 예제:**
```
feat : JWT 기반 인증 시스템 구현

- JWT 토큰 생성 및 검증 로직 추가
- 인증 미들웨어 구현
- 사용자 로그인/로그아웃 API 엔드포인트 추가

Closes #123
```

### 🤝 기여 워크플로우 (Contribution Workflow)

#### 1. Fork & Clone

```bash
# 1. GitHub에서 저장소 Fork

# 2. Fork한 저장소 클론
git clone https://github.com/YOUR_USERNAME/python-template.git
cd python-template

# 3. 원본 저장소를 upstream으로 추가
git remote add upstream https://github.com/ORIGINAL_OWNER/python-template.git
```

#### 2. 개발 환경 설정

```bash
# 1. 의존성 설치
uv sync

# 2. Pre-commit 설치
uv run pre-commit install

# 3. 환경 확인
uv run pytest
```

#### 3. 브랜치 생성

```bash
# feature 브랜치 생성
git checkout -b feat/your-feature-name

# bugfix 브랜치 생성
git checkout -b fix/your-bug-fix
```

**브랜치 명명 규칙:**
- `feat/기능명`: 새로운 기능
- `fix/버그명`: 버그 수정
- `refactor/리팩토링명`: 리팩토링
- `docs/문서명`: 문서 수정
- `test/테스트명`: 테스트 추가

#### 4. 개발 및 테스트

```bash
# 1. 코드 작성

# 2. 테스트 작성 (TDD 권장)
# tests/ 디렉토리에 테스트 파일 생성

# 3. 테스트 실행
uv run pytest

# 4. 코드 품질 검사
uv run ruff check .
uv run mypy .
uv run interrogate -vv app/

# 5. 커버리지 확인
uv run pytest --cov
```

#### 5. 커밋 및 푸시

```bash
# 1. 변경사항 스테이징
git add .

# 2. 커밋 (pre-commit 자동 실행)
git commit -m "feat : 새로운 기능 추가"

# 3. upstream 최신 변경사항 가져오기
git fetch upstream
git rebase upstream/main

# 4. Fork한 저장소에 푸시
git push origin feat/your-feature-name
```

#### 6. Pull Request 생성

1. GitHub에서 Fork한 저장소로 이동
2. "Compare & pull request" 버튼 클릭
3. PR 템플릿에 따라 내용 작성:
   - 변경사항 요약
   - 관련 이슈 번호
   - 테스트 방법
   - 체크리스트 확인

**PR 체크리스트:**
- [ ] 모든 테스트 통과
- [ ] 코드 커버리지 80% 이상
- [ ] 문서화율 90% 이상
- [ ] Pre-commit 훅 통과
- [ ] 타입 체크 통과
- [ ] 커밋 메시지 규칙 준수

#### 7. 코드 리뷰

- 리뷰어의 피드백에 성실히 응답
- 요청된 변경사항 반영
- 리뷰 승인 후 머지 가능

**코드 리뷰 기준:**
- 코드 가독성 및 유지보수성
- 테스트 충분성
- 보안 취약점 여부
- 성능 영향
- 문서화 완성도

### 💡 개발 팁 (Development Tips)

**로컬 개발 시 자주 사용하는 명령어:**
```bash
# 전체 품질 검사 (커밋 전 실행 권장)
uv run pre-commit run --all-files && uv run pytest --cov

# 변경된 파일만 빠르게 검사
uv run ruff check --fix .

# 테스트 실패 시 디버그 모드
uv run pytest -vv --pdb

# 특정 테스트만 반복 실행
uv run pytest tests/unit/test_user.py -k test_create_user -vv
```

**문제 해결:**

1. **Pre-commit이 너무 느릴 때:**
   ```bash
   # 특정 훅만 비활성화 (임시)
   SKIP=mypy git commit -m "message"
   ```

2. **타입 체크 오류가 많을 때:**
   ```bash
   # 점진적으로 타입 힌트 추가
   # type: ignore 주석 사용 (최소화)
   result = some_function()  # type: ignore[return-value]
   ```

3. **문서화율이 부족할 때:**
   ```bash
   # 부족한 부분 확인
   uv run interrogate -vv app/

   # 모든 public 함수에 docstring 추가
   ```

### 📚 추가 자료 (Additional Resources)

- **Ruff**: [docs.astral.sh/ruff](https://docs.astral.sh/ruff/)
- **Mypy**: [mypy-lang.org](https://mypy-lang.org/)
- **Pytest**: [docs.pytest.org](https://docs.pytest.org/)
- **Conventional Commits**: [conventionalcommits.org](https://www.conventionalcommits.org/)
- **Google Python Style Guide**: [google.github.io/styleguide/pyguide.html](https://google.github.io/styleguide/pyguide.html)

## 📦 Docker Stages 상세 (Docker Stages)

1.  **base**: OS 기본 패키지 및 `uv` 설치.
2.  **prod-deps**: 프로덕션용 Python 의존성 설치.
3.  **dev-deps**: 개발용 의존성 설치.
4.  **test**: CI/CD 파이프라인에서 테스트 수행용.
5.  **release**: 최종 배포용 경량 이미지 (Non-root 사용자 실행).
6.  **dev**: 로컬 개발용 (Git, Vim 등 도구 포함).
