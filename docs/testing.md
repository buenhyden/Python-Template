# 테스트 가이드 (Testing Guide)

이 문서는 프로젝트의 테스트 전략, 설정, 실행 방법에 대해 설명합니다.

## Pytest 설정

### 기본 설정 (pyproject.toml)

```toml
[tool.pytest.ini_options]
addopts = "--ignore=tests/load/ --cov=app --cov-report=term-missing -n auto --html=report.html --self-contained-html"
testpaths = ["tests"]
asyncio_default_fixture_loop_scope = "function"
asyncio_mode = "auto"
```

### 주요 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--ignore=tests/load/` | 부하 테스트 디렉토리 제외 |
| `--cov=app` | app/ 디렉토리 커버리지 측정 |
| `--cov-report=term-missing` | 누락된 라인 터미널 출력 |
| `-n auto` | CPU 코어 수에 맞춰 병렬 실행 |
| `--html=report.html` | HTML 테스트 보고서 생성 |
| `--self-contained-html` | CSS 포함 단일 HTML 파일 |
| `asyncio_mode=auto` | 비동기 테스트 자동 감지 |

## 커버리지 설정

### Coverage 설정

```toml
[tool.coverage.run]
source = ["app"]
omit = ["**/__init__.py", "tests/*"]

[tool.coverage.report]
fail_under = 80  # 80% 미만 시 실패
show_missing = true
```

**품질 기준:**
- 최소 커버리지: **80%**
- `__init__.py` 파일 제외
- 테스트 파일 제외

## Pytest 플러그인

### 설치된 플러그인

| 플러그인 | 버전 | 용도 |
|----------|------|------|
| `pytest` | >=9.0.2 | 테스트 프레임워크 |
| `pytest-asyncio` | >=1.3.0 | 비동기 테스트 지원 |
| `pytest-cov` | >=7.0.0 | 커버리지 측정 |
| `pytest-html` | >=4.1.1 | HTML 보고서 생성 |
| `pytest-mock` | >=3.15.1 | 모킹 기능 |
| `pytest-xdist` | >=3.8.0 | 병렬 테스트 실행 |

## 테스트 실행

### 기본 실행

```bash
# 모든 테스트 실행
uv run pytest

# 상세 출력
uv run pytest -v

# 매우 상세한 출력
uv run pytest -vv
```

### 커버리지 포함

```bash
# 커버리지 측정
uv run pytest --cov

# 커버리지 HTML 보고서
uv run pytest --cov --cov-report=html

# 보고서 확인
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

### 병렬 실행

```bash
# 자동 (CPU 코어 수만큼)
uv run pytest -n auto

# 특정 프로세스 수
uv run pytest -n 4
```

### 특정 테스트 실행

```bash
# 특정 파일
uv run pytest tests/unit/test_user.py

# 특정 테스트
uv run pytest tests/unit/test_user.py::test_create_user

# 패턴 매칭 (-k)
uv run pytest -k "test_user"

# 특정 마커
uv run pytest -m "slow"
```

### 실패 관련

```bash
# 실패한 테스트만 재실행
uv run pytest --lf

# 실패 시 즉시 중단
uv run pytest -x

# 첫 N개 실패 후 중단
uv run pytest --maxfail=3
```

### 디버깅

```bash
# 디버거 진입 (실패 시)
uv run pytest --pdb

# 즉시 디버거 진입
uv run pytest --trace

# 표준 출력 표시
uv run pytest -s
```

## 테스트 구조

### 디렉토리 구조

```
tests/
├── unit/           # 단위 테스트
│   ├── test_user.py
│   └── test_auth.py
├── integration/    # 통합 테스트 (선택)
│   └── test_api.py
├── load/           # 부하 테스트 (locust)
│   └── locustfile.py
├── conftest.py     # 공용 fixtures
└── __init__.py
```

### 테스트 파일 명명 규칙

- 파일명: `test_*.py` 또는 `*_test.py`
- 함수명: `test_*`
- 클래스명: `Test*`

### 예제 테스트

**단위 테스트:**
```python
import pytest
from app.services.user import UserService

def test_create_user():
    """사용자 생성 테스트."""
    user_service = UserService()
    user = user_service.create_user("test@example.com", "password")
    assert user.email == "test@example.com"

def test_create_user_duplicate(mocker):
    """중복 사용자 생성 실패 테스트."""
    user_service = UserService()
    mocker.patch.object(user_service, "exists", return_value=True)

    with pytest.raises(ValueError):
        user_service.create_user("test@example.com", "password")
```

**비동기 테스트:**
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """비동기 함수 테스트."""
    result = await some_async_function()
    assert result == expected_value
```

## Docker를 통한 테스트

### docker-compose.test.yml

프로젝트는 격리된 테스트 환경을 위해 Docker Compose를 사용합니다.

#### 포함된 서비스

| 서비스 | 이미지 | 용도 |
|--------|--------|------|
| `test` | Dockerfile (target: test) | 테스트 실행 |
| `postgres` | postgres:17-bookworm | PostgreSQL 데이터베이스 |
| `redis` | redis:7-alpine | Redis 캐시/브로커 |
| `kafka` | confluentinc/cp-kafka:7.5.0 | Kafka (KRaft 모드) |

#### 테스트 환경 변수 (45개)

**애플리케이션 설정:**
```yaml
PROJECT_NAME: "Test CI"
DEBUG: True
DEFAULT_PORT: 8000
SECRET_KEY: "test"
ALGORITHM: "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: 30
```

**데이터베이스:**
```yaml
DB_USER: postgres
DB_PASSWORD: password
DB_HOST: postgres
DB_PORT_WRITE: 5432
DB_PORT_READ: 5432
DB_NAME: app_db
```

**Redis:**
```yaml
REDIS_URL: redis://redis:6379
```

**Kafka:**
```yaml
KAFKA_BROKERS: ["kafka:9092"]
KAFKA_CONNECT_URL: http://localhost:8083
SCHEMA_REGISTRY_URL: http://localhost:8081
KAFKA_REST_PROXY_URL: http://localhost:8082
```

**외부 서비스 (로컬 개발용):**
```yaml
TEMPO_EXPORTER: http://localhost:4317
LOKI_URL: http://localhost:3100
OPENSEARCH_URL: http://localhost:9200
OLLAMA_URL: http://localhost:11434
N8N_URL: http://localhost:5678
```

### Docker 테스트 실행

```bash
# 테스트 빌드 및 실행
docker compose -f docker-compose.test.yml build test
docker compose -f docker-compose.test.yml run --rm test

# 전체 실행 (빌드 포함)
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit

# 정리
docker compose -f docker-compose.test.yml down -v
```

### PostgreSQL Health Check

테스트 서비스는 PostgreSQL이 준비될 때까지 대기합니다:

```yaml
depends_on:
  postgres:
    condition: service_healthy
```

Health check 설정:
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres"]
  interval: 5s
  timeout: 5s
  retries: 5
```

## 테스트 작성 가이드

### 1. AAA 패턴 사용

```python
def test_example():
    # Arrange (준비)
    user = User(email="test@example.com")

    # Act (실행)
    result = user.validate()

    # Assert (검증)
    assert result is True
```

### 2. Fixtures 활용

**conftest.py:**
```python
import pytest

@pytest.fixture
def db_session():
    """데이터베이스 세션 fixture."""
    session = create_session()
    yield session
    session.close()

@pytest.fixture
def sample_user():
    """샘플 사용자 fixture."""
    return User(email="test@example.com", name="Test User")
```

**사용:**
```python
def test_with_fixture(db_session, sample_user):
    db_session.add(sample_user)
    db_session.commit()
    assert sample_user.id is not None
```

### 3. Parametrize 사용

```python
@pytest.mark.parametrize("email,expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("@example.com", False),
])
def test_email_validation(email, expected):
    result = validate_email(email)
    assert result == expected
```

### 4. 모킹 사용

```python
def test_external_api(mocker):
    """외부 API 호출 모킹."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"status": "ok"}

    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_data()
    assert result["status"] == "ok"
```

### 5. 예외 테스트

```python
def test_exception():
    with pytest.raises(ValueError, match="Invalid input"):
        process_data(None)
```

## HTML 보고서

### 보고서 생성

pytest-html 플러그인이 자동으로 보고서를 생성합니다:

```bash
# 테스트 실행 (자동으로 report.html 생성)
uv run pytest

# 보고서 확인
open report.html  # macOS/Linux
start report.html  # Windows
```

### 보고서 내용

- 테스트 결과 요약
- 성공/실패/스킵 통계
- 각 테스트별 상세 정보
- 실패한 테스트의 스택 트레이스
- 실행 시간

## 테스트 팁

### 1. 빠른 피드백

```bash
# 변경된 파일과 관련된 테스트만
uv run pytest --testmon

# Watch 모드 (파일 변경 감지)
uv run pytest-watch
```

### 2. 테스트 격리

- 각 테스트는 독립적이어야 함
- 테스트 간 상태 공유 금지
- Fixture를 사용한 setup/teardown

### 3. 의미 있는 assert

```python
# 나쁜 예
assert result

# 좋은 예
assert result.status == 200, f"Expected 200, got {result.status}"
```

### 4. 테스트 마커 사용

```python
@pytest.mark.slow
def test_slow_operation():
    """느린 테스트."""
    pass

@pytest.mark.integration
def test_api_integration():
    """통합 테스트."""
    pass
```

실행:
```bash
# slow 테스트 제외
uv run pytest -m "not slow"

# integration 테스트만
uv run pytest -m "integration"
```

## CI/CD 통합

GitHub Actions에서 테스트가 자동으로 실행됩니다:

```yaml
- name: Run Tests via Docker Compose
  run: docker compose -f docker-compose.test.yml run --rm test
```

**자세한 내용은 [CI/CD 문서](ci-cd.md)를 참조하세요.**

## 트러블슈팅

### 테스트 실패 시 디버깅

```bash
# 상세 출력 + 디버거
uv run pytest -vv --pdb

# 로그 출력
uv run pytest -s --log-cli-level=DEBUG
```

### 커버리지가 낮을 때

```bash
# 누락된 라인 확인
uv run pytest --cov --cov-report=term-missing

# HTML 보고서로 확인
uv run pytest --cov --cov-report=html
open htmlcov/index.html
```

### 병렬 실행 문제

```bash
# 병렬 비활성화
uv run pytest -n 0

# 순차 실행
uv run pytest
```
