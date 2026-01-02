# UV 완전 가이드 (Complete UV Guide)

`uv`는 Rust로 작성된 극도로 빠른 Python 패키지 및 프로젝트 관리자입니다. `pip`, `pip-tools`, `poetry`, `pyenv`, `virtualenv`, `pipx` 등을 하나의 도구로 대체하며, 기존 도구 대비 **10-100배 빠른 성능**을 제공합니다.

## 목차

- [소개](#소개)
- [설치 및 업그레이드](#설치-및-업그레이드)
- [프로젝트 관리](#프로젝트-관리)
- [의존성 관리](#의존성-관리)
- [가상환경 관리](#가상환경-관리)
- [Python 버전 관리](#python-버전-관리)
- [스크립트 실행](#스크립트-실행)
- [도구 실행 (uvx)](#도구-실행-uvx)
- [pip 호환 모드](#pip-호환-모드)
- [고급 기능](#고급-기능)
- [설정 파일](#설정-파일)
- [실전 예제](#실전-예제)
- [트러블슈팅](#트러블슈팅)

## 소개

### 특징 및 장점

1. **극도로 빠름**
   - Rust로 작성됨
   - 병렬 다운로드 및 설치
   - 전역 캐시 공유
   - pip 대비 10-100배 빠른 성능

2. **통합 관리**
   - 패키지 관리 (pip)
   - 의존성 잠금 (pip-tools)
   - 프로젝트 관리 (poetry)
   - Python 버전 관리 (pyenv)
   - 가상환경 (virtualenv)
   - 도구 실행 (pipx)

3. **재현 가능한 빌드**
   - `uv.lock` 자동 생성
   - 플랫폼 독립적 해결
   - 정확한 버전 고정

4. **현대적 통합**
   - `pyproject.toml` 중심
   - Workspace 지원
   - Dependency Groups

### 대체하는 도구들

| 도구 | uv 대응 기능 |
|------|--------------|
| `pip` | `uv pip` |
| `pip-tools` | `uv pip compile`, `uv pip sync` |
| `poetry` | `uv init`, `uv add`, `uv sync` |
| `pyenv` | `uv python install` |
| `virtualenv` | `uv venv` |
| `pipx` | `uvx` / `uv tool run` |

## 설치 및 업그레이드

### Linux/macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows

**PowerShell:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**winget:**
```powershell
winget install --id=astral-sh.uv -e
```

### pip로 설치 (권장하지 않음)

```bash
pip install uv
```

> **권장사항**: 스탠드얼론 설치를 사용하여 Python 환경과 독립적으로 사용

### 업그레이드

```bash
# 자체 업그레이드
uv self update

# 또는 재설치
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 설치 확인

```bash
uv --version
# 또는
uv version
```

## 프로젝트 관리

### 새 프로젝트 초기화

```bash
# 현재 디렉토리에 초기화
uv init

# 새 디렉토리에 프로젝트 생성
uv init my-project
cd my-project
```

**생성되는 파일:**
- `pyproject.toml` - 프로젝트 메타데이터 및 의존성
- `.python-version` - Python 버전 고정 (선택)
- `README.md` - 프로젝트 소개
- `src/my_project/__init__.py` - 패키지 초기화

### 프로젝트 동기화

```bash
# 모든 의존성 설치
uv sync

# 개발 의존성 제외
uv sync --no-dev

# 특정 Dependency Group만
uv sync --group docs

# Dry run (실제 설치하지 않음)
uv sync --dry-run
```

### pyproject.toml 통합

uv는 `pyproject.toml`을 중심으로 모든 설정을 관리합니다:

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn>=0.20.0",
]

[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]
```

## 의존성 관리

### 패키지 추가

```bash
# 기본 의존성 추가
uv add fastapi uvicorn

# 개발 의존성 추가
uv add --dev pytest ruff mypy

# 특정 버전 지정
uv add "fastapi>=0.100.0"
uv add "django~=4.2"

# 최신 버전으로 업그레이드하며 추가
uv add --upgrade fastapi
```

### 패키지 제거

```bash
# 패키지 제거
uv remove fastapi

# 개발 의존성 제거
uv remove --dev pytest
```

### 의존성 잠금

```bash
# uv.lock 생성/업데이트
uv lock

# 업그레이드 가능한 패키지 확인하며 잠금
uv lock --upgrade

# 특정 패키지만 업그레이드
uv lock --upgrade-package fastapi
```

### 의존성 업데이트

```bash
# 모든 의존성 업데이트
uv sync --upgrade

# 특정 패키지만 업데이트
uv sync --upgrade-package fastapi

# 재설치
uv sync --reinstall
```

### Dependency Groups

pyproject.toml에서 그룹별로 의존성 관리:

```toml
[dependency-groups]
dev = ["pytest", "ruff"]
docs = ["mkdocs", "mkdocs-material"]
test = ["pytest-cov", "pytest-xdist"]
```

**사용:**
```bash
# 특정 그룹만 설치
uv sync --group docs

# 여러 그룹
uv sync --group docs --group test

# 그룹 제외
uv sync --no-group dev
```

### 플랫폼 독립적 해결

```bash
# 모든 플랫폼에서 동작하는 uv.lock 생성
uv lock --universal

# 특정 플랫폼용
uv lock --python-platform linux
uv lock --python-platform windows
uv lock --python-platform darwin
```

### 의존성 오버라이드

특정 의존성 버전 강제:

```toml
[tool.uv]
override-dependencies = [
    "numpy==1.24.0",
]
```

또는 특정 패키지 제약 무시:

```toml
[tool.uv]
constraint-dependencies = [
    "some-package<2.0",
]
```

## 가상환경 관리

### 가상환경 생성

```bash
# 기본 (.venv)
uv venv

# 특정 Python 버전
uv venv --python 3.13
uv venv --python python3.12

# 커스텀 경로
uv venv /path/to/venv

# 시스템 패키지 포함
uv venv --system-site-packages
```

### 가상환경 활성화

```bash
# Linux/macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\activate

# Windows (CMD)
.venv\Scripts\activate.bat
```

### 자동 활성화 (uv run)

`uv run` 사용 시 가상환경이 자동으로 활성화됩니다:

```bash
# 가상환경 활성화하지 않아도 됨
uv run python script.py
uv run pytest
```

## Python 버전 관리

### Python 설치

```bash
# 특정 버전 설치
uv python install 3.13
uv python install 3.12.0

# 최신 버전 설치
uv python install

# 여러 버전 설치
uv python install 3.11 3.12 3.13
```

### 설치된 Python 확인

```bash
# 사용 가능한 버전 목록
uv python list

# 설치된 버전만
uv python list --only-installed
```

### Python 버전 고정

```bash
# 프로젝트에 Python 버전 고정
uv python pin 3.13

# .python-version 파일 생성됨
cat .python-version
# 3.13
```

### 자동 Python 다운로드

uv는 필요한 Python 버전이 없으면 자동으로 다운로드합니다:

```bash
# Python 3.13이 없어도 자동 설치
uv venv --python 3.13
```

## 스크립트 실행

### uv run 기본 사용

```bash
# Python 스크립트 실행
uv run python script.py

# 모듈 실행
uv run python -m http.server

# 애플리케이션 실행
uv run uvicorn app.main:app --reload

# 테스트 실행
uv run pytest

# 린팅
uv run ruff check .
```

### Inline Script Dependencies

스크립트 파일에 직접 의존성 명시:

```python
# /// script
# dependencies = [
#   "requests>=2.28",
#   "beautifulsoup4",
# ]
# ///

import requests
from bs4 import BeautifulSoup

response = requests.get("https://example.com")
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title.string)
```

**실행:**
```bash
# uv가 자동으로 의존성 설치 후 실행
uv run script.py
```

## 도구 실행 (uvx)

전역 설치 없이 도구 실행:

### 기본 사용

```bash
# 도구 일회성 실행
uvx ruff check .
uvx black .
uvx mypy .

# 또는
uv tool run ruff check .
```

### 도구 설치 및 관리

```bash
# 도구 설치
uv tool install ruff

# 설치된 도구 목록
uv tool list

# 도구 업그레이드
uv tool upgrade ruff

# 도구 제거
uv tool uninstall ruff
```

### 실용 예제

```bash
# Jupyter Notebook 실행
uvx jupyter notebook

# HTTP 서버
uvx -p 3.12 python -m http.server

# Cookiecutter
uvx cookiecutter gh:user/template
```

## pip 호환 모드

### pip 명령어 대응

| pip 명령어 | uv 대응 | 설명 |
|------------|---------|------|
| `pip install package` | `uv pip install package` | 패키지 설치 |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` | requirements 파일 설치 |
| `pip uninstall package` | `uv pip uninstall package` | 패키지 제거 |
| `pip list` | `uv pip list` | 설치된 패키지 목록 |
| `pip freeze` | `uv pip freeze` | 현재 환경 내보내기 |
| `pip show package` | `uv pip show package` | 패키지 정보 |
| `pip-compile` | `uv pip compile` | 의존성 컴파일 |
| `pip-sync` | `uv pip sync` | 정확한 동기화 |

### pip-tools 대체

```bash
# requirements.in에서 requirements.txt 생성
uv pip compile requirements.in -o requirements.txt

# 모든 플랫폼용 requirements
uv pip compile requirements.in --universal -o requirements.txt

# requirements.txt와 정확히 동기화
uv pip sync requirements.txt
```

### 가상환경에서 사용

```bash
# 가상환경 생성
uv venv

# 활성화
source .venv/bin/activate

# pip 명령어 사용
uv pip install fastapi
uv pip list
```

## 고급 기능

### Workspaces

멀티 패키지 프로젝트 관리:

**프로젝트 구조:**
```
my-workspace/
├── pyproject.toml
├── packages/
│   ├── package-a/
│   │   └── pyproject.toml
│   └── package-b/
│       └── pyproject.toml
```

**루트 pyproject.toml:**
```toml
[tool.uv.workspace]
members = ["packages/*"]
```

**사용:**
```bash
# 워크스페이스 전체 동기화
uv sync

# 특정 패키지에서 작업
cd packages/package-a
uv add requests
```

### 빌드 및 배포

```bash
# 패키지 빌드
uv build

# PyPI에 배포
uv publish

# 테스트 PyPI
uv publish --publish-url https://test.pypi.org/legacy/
```

### 캐시 관리

```bash
# 캐시 디렉토리 확인
uv cache dir

# 캐시 정리
uv cache clean

# 특정 패키지 캐시 제거
uv cache clean package-name

# 캐시 상태 확인
uv cache stat
```

### 빌드 격리

특정 빌드 환경 설정:

```toml
[tool.uv]
no-build-isolation = false
no-build-isolation-package = ["numpy"]
```

### 인덱스 설정

```toml
[tool.uv]
index-url = "https://pypi.org/simple"
extra-index-url = [
    "https://private.pypi.org/simple",
]
```

또는 환경 변수:
```bash
export UV_INDEX_URL="https://pypi.org/simple"
```

## 설정 파일

### pyproject.toml

```toml
[tool.uv]
# 패키지 모드 (라이브러리 개발)
package = true

# 관리 모드 (프로젝트 관리 강화)
managed = true

# 의존성 오버라이드
override-dependencies = [
    "numpy==1.24.0",
]

# 캐시 디렉토리
cache-dir = ".uv-cache"

# 인덱스 URL
index-url = "https://pypi.org/simple"

# 빌드 격리
no-build-isolation = false
```

### 환경 변수

| 변수 | 설명 |
|------|------|
| `UV_INDEX_URL` | PyPI 인덱스 URL |
| `UV_CACHE_DIR` | 캐시 디렉토리 |
| `UV_PYTHON` | 사용할 Python 경로 |
| `UV_PROJECT_ENVIRONMENT` | 가상환경 경로 |
| `UV_COMPILE_BYTECODE` | Bytecode 컴파일 (1/0) |
| `UV_LINK_MODE` | 링크 모드 (copy/hardlink/symlink) |

## 실전 예제

### 일반적인 워크플로우

```bash
# 1. 프로젝트 클론
git clone <repository>
cd <project>

# 2. Python 버전 확인/설치
uv python install 3.13

# 3. 의존성 설치
uv sync

# 4. 개발
uv run uvicorn app.main:app --reload

# 5. 테스트
uv run pytest

# 6. 새 패키지 추가
uv add requests

# 7. 의존성 업데이트
uv lock --upgrade
uv sync
```

### CI/CD 통합

**GitHub Actions:**
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v5
  with:
    version: "latest"
    enable-cache: true

- name: Set up Python
  run: uv python install 3.13

- name: Install dependencies
  run: uv sync

- name: Run tests
  run: uv run pytest
```

### Docker 통합

**Dockerfile:**
```dockerfile
FROM python:3.13-slim

# uv 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 의존성 파일 복사
COPY pyproject.toml uv.lock ./

# 의존성 설치
RUN uv sync --frozen --no-dev

# 소스 복사
COPY ./src ./src

# 실행
CMD ["uv", "run", "uvicorn", "app.main:app"]
```

### 마이그레이션

**pip에서 마이그레이션:**
```bash
# requirements.txt에서 pyproject.toml 생성
uv init

# requirements.txt의 패키지 추가
cat requirements.txt | xargs uv add
```

**poetry에서 마이그레이션:**
```bash
# pyproject.toml은 그대로 사용 가능
uv sync

# poetry.lock 제거
rm poetry.lock

# uv.lock 생성
uv lock
```

## 트러블슈팅

### 의존성 충돌

```bash
# 상세 로그 출력
uv sync -v

# 의존성 트리 확인
uv pip tree

# 특정 패키지 의존성 확인
uv pip show package-name
```

### 캐시 문제

```bash
# 캐시 정리 후 재설치
uv cache clean
uv sync --reinstall
```

### 잠금 파일 문제

```bash
# 잠금 파일 재생성
rm uv.lock
uv lock

# 잠금 검증
uv lock --check
```

### Python 버전 문제

```bash
# 사용 가능한 Python 확인
uv python list

# 특정 버전 설치
uv python install 3.13

# 프로젝트 Python 재설정
uv python pin 3.13
```

### 빌드 오류

```bash
# 빌드 격리 비활성화
uv sync --no-build-isolation

# 특정 패키지만
uv sync --no-build-isolation-package numpy
```

## 추가 자료

- **공식 문서**: https://docs.astral.sh/uv/
- **GitHub**: https://github.com/astral-sh/uv
- **Discord 커뮤니티**: https://discord.gg/astral-sh
- **변경 로그**: https://github.com/astral-sh/uv/releases

## 자주 사용하는 명령어 치트시트

```bash
# 프로젝트 관리
uv init                    # 프로젝트 초기화
uv sync                    # 의존성 동기화
uv add <package>           # 패키지 추가
uv remove <package>        # 패키지 제거
uv lock                    # 의존성 잠금

# Python 관리
uv python install 3.13     # Python 설치
uv python list             # Python 목록
uv python pin 3.13         # Python 고정

# 실행
uv run <command>           # 명령 실행
uvx <tool>                 # 도구 일회성 실행

# 가상환경
uv venv                    # 가상환경 생성
uv venv --python 3.13      # 특정 버전으로 생성

# pip 호환
uv pip install <package>   # 패키지 설치
uv pip list                # 패키지 목록
uv pip compile             # requirements 컴파일
uv pip sync                # requirements 동기화

# 유틸리티
uv cache clean             # 캐시 정리
uv self update             # uv 업데이트
uv --version               # 버전 확인
```
