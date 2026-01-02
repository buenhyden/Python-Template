# 개발 환경 (Development Environment)

이 문서는 프로젝트의 개발 환경 설정과 도구에 대해 설명합니다.

## 개발 도구 스택

### uv - Python 패키지 관리자

이 프로젝트는 `uv`를 사용하여 Python 패키지와 의존성을 관리합니다.

**특징:**
- pip 대비 10-100배 빠른 성능
- 의존성 잠금 파일(`uv.lock`) 자동 관리
- 가상환경 자동 생성 및 관리

**주요 명령어:**
```bash
# 의존성 설치
uv sync

# 패키지 추가
uv add package-name

# 개발 의존성 추가
uv add --dev package-name

# 패키지 제거
uv remove package-name

# 가상환경에서 명령 실행
uv run command
```

## pyproject.toml 설정

### 프로젝트 메타데이터

```toml
[project]
name = "python-template"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = ["pydantic>=2.12.5"]
```

### 개발 의존성

프로젝트는 다음 개발 도구들을 사용합니다:

| 도구 | 버전 | 용도 |
|------|------|------|
| `commitizen` | >=4.11.0 | 커밋 메시지 관리 및 버전 관리 |
| `detect-secrets` | >=1.5.0 | 비밀 정보 검사 |
| `httpx` | >=0.28.1 | HTTP 클라이언트 |
| `mypy` | >=1.19.1 | 정적 타입 체크 |
| `pip-audit` | >=2.10.0 | 패키지 취약점 검사 |
| `pre-commit` | >=4.5.1 | Git hook 관리 |
| `pytest` | >=9.0.2 | 테스트 프레임워크 |
| `pytest-asyncio` | >=1.3.0 | 비동기 테스트 |
| `pytest-cov` | >=7.0.0 | 커버리지 측정 |
| `pytest-html` | >=4.1.1 | HTML 테스트 보고서 |
| `pytest-mock` | >=3.15.1 | 모킹 |
| `pytest-xdist` | >=3.8.0 | 병렬 테스트 |
| `ruff` | >=0.14.10 | 린팅 및 포맷팅 |

### Ruff 설정

**기본 설정:**
```toml
[tool.ruff]
line-length = 120
target-version = "py313"
```

**린트 규칙 (18개 카테고리):**

| 코드 | 규칙 | 설명 |
|------|------|------|
| `A` | flake8-builtins | 내장 함수 shadowing 방지 |
| `ARG` | unused-arguments | 미사용 인자 검사 |
| `ASYNC` | async optimization | 비동기 코드 최적화 |
| `B` | flake8-bugbear | 설계 문제 검사 |
| `C4` | flake8-comprehensions | Comprehension 개선 |
| `C90` | mccabe | 복잡도 검사 (≤10) |
| `D` | pydocstyle | 문서화 규칙 (Google 스타일) |
| `E` | pycodestyle errors | 코드 스타일 에러 |
| `ERA` | eradicate | 주석 처리된 코드 검사 |
| `F` | Pyflakes | 논리 오류 검사 |
| `FURB` | refurb | 현대적 리팩토링 제안 |
| `I` | isort | Import 정렬 |
| `LOG` | logging | 로깅 가이드 준수 |
| `N` | pep8-naming | PEP 8 명명 규칙 |
| `NPY` | NumPy | NumPy 전용 규칙 |
| `PERF` | performance | 성능 최적화 |
| `PL` | Pylint | Pylint 규칙 |
| `PT` | flake8-pytest-style | Pytest 베스트 프랙티스 |
| `RUF` | Ruff-specific | Ruff 전용 규칙 |
| `S` | flake8-bandit | 보안 검사 |
| `SIM` | flake8-simplify | 코드 간소화 |
| `T20` | flake8-print | print문 제한 |
| `TCH` | flake8-type-checking | 타입 체크 최적화 |
| `TID` | flake8-tidy-imports | Import 정돈 |
| `UP` | pyupgrade | 최신 문법 사용 |

**파일별 예외:**
```toml
[tool.ruff.lint.per-file-ignores]
"app/core/config/settings.py" = ["S105", "S106"]  # 하드코딩된 비밀번호 허용
"tests/**/*" = ["S101", "S105", "S106", "S110"]  # assert문, 테스트 비밀번호 허용
```

### Mypy 설정

**Strict Mode 활성화:**
```toml
[tool.mypy]
python_version = "3.13"
strict = true
ignore_missing_imports = true
check_untyped_defs = true
disallow_untyped_calls = true
warn_unused_ignores = true
plugins = ["pydantic.mypy"]
```

**테스트 코드 예외:**
```toml
[[tool.mypy.overrides]]
module = "tests.*"
allow_untyped_defs = true
```

### Commitizen 설정

**Semantic Versioning 및 Changelog 자동화:**
```toml
[tool.commitizen]
name = "cz_conventional_commits"
version_provider = "pep621"
version_scheme = "semver"
tag_format = "v$version"
update_changelog_on_bump = true
major_version_zero = true
```

**사용 명령어:**
```bash
# 커밋 생성 (대화형)
uv run cz commit

# 버전 범프 및 태그 생성
uv run cz bump

# CHANGELOG 생성
uv run cz changelog
```

## Pre-commit Hooks

### 설치

```bash
uv run pre-commit install
```

### 포함된 Hooks (14개)

#### 1. 파일 검사 (pre-commit-hooks)

| Hook | 설명 |
|------|------|
| `check-json` | JSON 문법 검사 |
| `check-ast` | Python AST 검사 |
| `check-docstring-first` | Docstring 위치 검사 |
| `pretty-format-json` | JSON 자동 포맷팅 |
| `check-added-large-files` | 대용량 파일 검사 (50MB) |
| `check-case-conflict` | 파일명 대소문자 충돌 검사 |
| `check-merge-conflict` | Merge conflict 검사 |
| `check-yaml` | YAML 문법 검사 |
| `check-toml` | TOML 문법 검사 |
| `end-of-file-fixer` | 파일 끝 줄바꿈 |
| `mixed-line-ending` | 줄바꿈 통일 |
| `trailing-whitespace` | 후행 공백 제거 |
| `debug-statements` | 디버그 문 검사 |
| `name-tests-test` | 테스트 파일명 검사 |

#### 2. YAML 포맷팅 (yamlfmt)

YAML 파일 자동 포맷팅

#### 3. 맞춤법 검사 (codespell)

코드 및 주석의 맞춤법 검사

#### 4. Ruff (린팅 & 포맷팅)

```yaml
- id: ruff
  args: [--fix]
- id: ruff-format
```

#### 6. Mypy (타입 체크)

추가 타입 패키지 포함:
- `pydantic>=2.12.5`
- `types-requests`
- `types-sqlalchemy`
- `types-httpx`

#### 7. detect-secrets (비밀 정보 검사)

```yaml
- id: detect-secrets
  args: ["--baseline", ".secrets.baseline"]
  exclude: uv.lock
```

#### 8. uv lock 검사 (로컬 훅)

```yaml
- id: uv-lock-check
  entry: uv lock --check
```

pyproject.toml 또는 uv.lock 변경 시 동기화 검사

#### 9. pip-audit (로컬 훅)

```yaml
- id: pip-audit
  entry: uv run pip-audit
```

의존성 보안 취약점 검사

#### 10. commitizen (커밋 메시지 검사)

```yaml
- id: commitizen
  stages: [commit-msg]
```

Conventional Commits 형식 검사

### 수동 실행

```bash
# 모든 훅 실행
uv run pre-commit run --all-files

# 특정 훅만 실행
uv run pre-commit run ruff --all-files
uv run pre-commit run mypy --all-files

# 스테이징된 파일만 검사
uv run pre-commit run
```

### 훅 건너뛰기 (비권장)

```bash
# 모든 훅 건너뛰기
git commit --no-verify -m "message"

# 특정 훅만 건너뛰기
SKIP=mypy git commit -m "message"
```

## 개발 워크플로우

### 1. 프로젝트 설정

```bash
# 저장소 클론
git clone <repository>
cd <project>

# 의존성 설치
uv sync

# Pre-commit 설치
uv run pre-commit install

# 커밋 템플릿 설정
git config commit.template .gitmessage
```

### 2. 코드 작성

```bash
# 브랜치 생성
git checkout -b feat/feature-name

# 코드 작성 및 테스트
uv run pytest

# 코드 품질 검사
uv run ruff check .
uv run mypy .
```

### 3. 커밋

```bash
# Commitizen 사용 (권장)
uv run cz commit

# 또는 수동 커밋 (pre-commit 자동 실행)
git add .
git commit
```

### 4. 푸시 및 PR

```bash
# 푸시
git push origin feat/feature-name

# GitHub에서 PR 생성
```

## 환경 변수

개발 시 필요한 환경 변수는 `.env` 파일에 설정하세요 (gitignore 처리됨).

**예제 `.env`:**
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=app_db
REDIS_URL=redis://localhost:6379
```

## 트러블슈팅

### Pre-commit이 느릴 때

```bash
# 특정 훅만 비활성화
SKIP=mypy git commit -m "message"

# 캐시 정리
uv run pre-commit clean
```

### 의존성 충돌

```bash
# 의존성 재설치
uv sync --reinstall

# 캐시 정리
uv cache clean
```

### 타입 체크 오류

```bash
# 점진적으로 타입 힌트 추가
# type: ignore 주석 사용 (최소화)
result = function()  # type: ignore[return-value]
```
