# Pre-commit 가이드 (Pre-commit Guide)

이 문서는 프로젝트에서 사용하는 git hook 관리 도구인 **Pre-commit**의 설정과 사용법에 대해 상세히 설명합니다.

## 개요

Pre-commit은 git commit 명령을 실행할 때 자동으로 실행되는 스크립트입니다. 코드 품질을 유지하고, 잘못된 코드가 저장소에 커밋되는 것을 방지합니다.

**설정 파일 위치:** `.pre-commit-config.yaml`

## 🚀 시작하기

### 설치

프로젝트 의존성을 설치할 때 함께 설치되지만, git hook을 활성화하려면 다음 명령어를 한 번 실행해야 합니다.

```bash
uv run pre-commit install
```

설치가 완료되면 `.git/hooks/pre-commit` 파일이 생성됩니다.

### 실행 방법

보통 `git commit` 시 자동으로 실행되지만, 수동으로 실행할 수도 있습니다.

```bash
# 모든 파일에 대해 실행 (추천)
uv run pre-commit run --all-files

# 스테이징된 파일만 검사
uv run pre-commit run

# 특정 훅만 실행
uv run pre-commit run ruff --all-files
```

## 🛠️ 포함된 Hooks 상세

이 프로젝트에는 총 14개 이상의 품질 검사 도구가 포함되어 있습니다.

### 1. 기본 검사 (Pre-commit Hooks)
`https://github.com/pre-commit/pre-commit-hooks`

| Hook ID | 설명 |
|---------|------|
| `check-json` | JSON 문법 검사 |
| `check-ast` | Python 추상 구문 트리(AST) 유효성 검사 |
| `check-docstring-first` | Docstring이 코드보다 먼저 나오는지 검사 |
| `pretty-format-json` | JSON 파일 표준 포맷팅 및 정렬 |
| `check-added-large-files` | 50MB 이상의 대용량 파일 커밋 방지 |
| `check-case-conflict` | 대소문자만 다른 파일명 충돌 방지 (Windows/macOS 호환성) |
| `check-merge-conflict` | 커밋에 merge conflict 마커가 남아있는지 검사 |
| `check-yaml` | YAML 문법 검사 |
| `check-toml` | TOML 문법 검사 |
| `end-of-file-fixer` | 파일 끝에 빈 줄(newline) 하나만 있도록 수정 |
| `mixed-line-ending` | 줄바꿈 문자(LF/CRLF) 통일 |
| `trailing-whitespace` | 줄 끝의 불필요한 공백 제거 |
| `debug-statements` | 실수로 남긴 `pdb`, `breakpoint()` 등 디버그 코드 감지 |
| `name-tests-test` | 테스트 파일 이름이 `test_`로 시작하거나 `_test.py`로 끝나는지 검사 |

### 2. 코드 스타일 & 포맷팅

#### YAML Formatter
- **Repo**: `https://github.com/google/yamlfmt`
- **Hook**: `yamlfmt`
- **설명**: YAML 파일을 구글 스타일로 자동 포맷팅합니다.

#### Codespell (맞춤법 검사)
- **Repo**: `https://github.com/codespell-project/codespell`
- **Hook**: `codespell`
- **설명**: 코드, 주석, 문서의 영어 맞춤법 오류를 찾아냅니다.

#### Ruff (Linting & Formatting)
- **Repo**: `https://github.com/astral-sh/ruff-pre-commit`
- **Hooks**: `ruff`, `ruff-format`
- **설명**: Python 코드를 린팅하고 포맷팅합니다. `pyproject.toml` 설정을 따릅니다.

### 3. 정적 분석 & 타입 체크

#### Mypy (Type Checking)
- **Repo**: `https://github.com/pre-commit/mirrors-mypy`
- **Hook**: `mypy`
- **설명**: 정적 타입 검사를 수행합니다. `pydantic`, `httpx` 등 필요한 타입 스텁이 포함되어 있습니다.

### 4. 보안 및 의존성

#### Detect Secrets
- **Repo**: `https://github.com/Yelp/detect-secrets`
- **Hook**: `detect-secrets`
- **설명**: API 키, 비밀번호 같은 민감 정보가 커밋되는 것을 방지합니다. 베이스라인 파일(`.secrets.baseline`)을 기준으로 검사합니다.

#### uv lock check (Local)
- **Hook**: `uv-lock-check`
- **설명**: `pyproject.toml`과 `uv.lock` 파일이 동기화되어 있는지 검사합니다.

#### Pip Audit (Local)
- **Hook**: `pip-audit`
- **설명**: 설치된 패키지에 알려진 보안 취약점이 있는지 검사합니다.

### 5. 커밋 메시지

#### Commitizen
- **Repo**: `https://github.com/commitizen-tools/commitizen`
- **Hook**: `commitizen`
- **Stage**: `commit-msg`
- **설명**: 커밋 메시지가 Conventional Commits 규칙을 따르는지 검사합니다.

## ❓ 문제 해결 (Troubleshooting)

### Lock 파일 동기화 오류
`uv-lock-check` 실패 시:
```bash
uv lock
git add uv.lock
```

### 비밀 정보 오탐지 (False Positive)
`detect-secrets`가 비밀이 아닌 값을 감지했을 때:
```bash
# 베이스라인 업데이트 (해당 값을 허용 목록에 추가)
uv run detect-secrets scan > .secrets.baseline
git add .secrets.baseline
```

### 훅 건너뛰기
긴급한 핫픽스 등으로 인해 검사를 건너뛰어야 할 때 (비권장):
```bash
git commit --no-verify -m "fix: urgent hotfix"
```

### 특정 훅만 건너뛰기
```bash
SKIP=mypy,pip-audit git commit -m "feat: wip"
```

## 캐시 관리

Pre-commit은 자체적으로 환경을 캐싱합니다. 문제가 발생하거나 디스크 공간을 확보하려면:

```bash
# 캐시 삭제
uv run pre-commit clean
```
