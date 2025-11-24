# 🐍 Python FastAPI Template

**깃허브 템플릿 저장소로 사용할 수 있는 Python FastAPI 프로젝트 템플릿**

이 템플릿은 Poetry, Docker, Linting, Pre-commit Hooks, CI/CD가 미리 구성되어 있어 즉시 사용 가능한 프로젝트 기반을 제공합니다. **Git Flow**를 적용한 새 프로젝트를 시작할 때 최적화된 설정입니다.

---

## ✨ 주요 기능

- **🚀 FastAPI**: 고성능 비동기 웹 프레임워크
- **📦 Poetry**: 현대적인 의존성 관리 및 패키징
- **🐳 Docker**: 컨테이너화된 개발 및 배포 환경
- **⚡ Ruff**: 빠른 Python 린터 및 코드 포매터
- **� Mypy**: 정적 타입 검사
- **�🔒 Pre-commit**: 자동화된 Git hooks로 코드 품질 보장
- **✅ Pytest**: 강력한 테스트 프레임워크
- **🔄 CI/CD**: Git Flow 지원 GitHub Actions 워크플로우

---

## 📋 필수 요구 사항

- **Python** 3.12 이상
- **Docker** 및 **Docker Compose**
- **Poetry** (의존성 관리)
- **Git** (버전 관리)

---

## 🛠️ 템플릿 사용 방법

### 1. 템플릿으로 새 저장소 생성

GitHub에서 이 저장소를 템플릿으로 사용하여 새 프로젝트를 생성합니다:

1. 저장소 페이지에서 **"Use this template"** 버튼 클릭
2. 새 저장소 이름 및 설정 입력
3. **"Create repository from template"** 클릭

### 2. 로컬 개발 환경 설정

```bash
# 새로 생성한 저장소 클론
git clone <your-repository-url>
cd <your-project-name>

# Poetry를 사용하여 의존성 설치
poetry install

# 가상 환경 활성화
poetry shell

# Pre-commit hooks 설치
pre-commit install

# Git 커밋 템플릿 설정
git config commit.template .gitmessage
```

### 3. 환경 변수 설정

```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env

# 필요한 환경 변수 수정
```

---

## 🌿 Git Flow 적용

이 템플릿은 **Git Flow** 브랜치 전략을 지원합니다. 새 프로젝트에서 Git Flow를 초기화하려면:

```bash
# Git Flow 초기화 (명령어가 설치되어 있다면)
git flow init

# 또는 수동으로 브랜치 생성
git checkout -b develop
git push -u origin develop
```

### Git Flow 브랜치 구조

- **main**: 프로덕션 릴리스
- **develop**: 개발 통합 브랜치
- **feature/**: 새로운 기능 개발 (`feature/feature-name`)
- **release/**: 릴리스 준비 (`release/v1.0.0`)
- **hotfix/**: 긴급 버그 수정 (`hotfix/bug-description`)

### CI/CD 트리거

GitHub Actions는 다음 브랜치에서 자동으로 실행됩니다:

- **Push**: `main`, `master`, `develop`, `release/**`, `hotfix/**`
- **Pull Request**: `main`, `master`, `develop`

---

## 🚀 사용 방법

### 로컬 실행

```bash
# 애플리케이션 시작
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker로 실행

```bash
# Docker Compose로 빌드 및 실행
docker-compose up --build
```

애플리케이션은 `http://localhost:8000`에서 접근 가능합니다.

### 📚 API 문서

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 💻 개발

### 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/unit/test_example.py

# 커버리지 포함
pytest --cov=src
```

### 린팅 및 포매팅

```bash
# Ruff로 린트 검사 및 자동 수정
ruff check . --fix

# 코드 포매팅
ruff format .

# Mypy로 타입 검사
mypy src/

# Pre-commit으로 모든 검사 실행
pre-commit run --all-files
```

---

## 📂 프로젝트 구조

```
.
├── .github/
│   └── workflows/          # 🤖 CI/CD 워크플로우 (Git Flow 지원)
├── deploy/                 # 🚀 배포 관련 설정
├── logs/                   # 📝 애플리케이션 로그
├── src/                    # 🧠 메인 소스 코드
│   ├── core/               # ⚙️ 핵심 기능 (설정, 로거 등)
│   ├── db/                 # 💾 데이터베이스 연결 및 모델
│   ├── main.py             # 🏁 FastAPI 애플리케이션 진입점
│   └── ...
├── tests/                  # 🧪 테스트 코드
│   ├── unit/               # 단위 테스트
│   ├── integration/        # 통합 테스트
│   └── ...
├── .dockerignore           # Docker 빌드 제외 파일
├── .env.example            # 환경 변수 예제
├── .gitignore              # Git 추적 제외 파일
├── .gitmessage             # 📝 Git 커밋 메시지 템플릿
├── .pre-commit-config.yaml # 🔒 Pre-commit hooks 설정
├── Dockerfile              # 🐳 Docker 이미지 정의
├── docker-compose.yml      # 🐙 Docker Compose 구성
├── docker-compose.test.yml # 🧪 테스트용 Docker Compose
├── poetry.lock             # 📌 잠긴 의존성 버전
├── pyproject.toml          # 📦 Poetry 및 도구 설정
└── README.md               # 📖 이 문서
```

---

## 🔧 설정 파일 개요

### `pyproject.toml`
- Poetry 의존성 및 메타데이터
- Ruff 린팅 및 포매팅 규칙
- Mypy 타입 검사 설정
- Pytest 테스트 옵션

### `.pre-commit-config.yaml`
커밋 전 자동으로 실행되는 검사:
- JSON/YAML 포맷 검사
- 파일 크기 제한
- Trailing whitespace 제거
- Ruff 린팅 및 포매팅
- Mypy 타입 검사

### `.github/workflows/backend-ci.yml`
Git Flow 지원 CI/CD 파이프라인:
1. Pre-commit 검사
2. Docker 이미지 빌드
3. 테스트 실행

---

## 📝 커밋 메시지 규칙

이 프로젝트는 `.gitmessage` 템플릿을 사용합니다:

```bash
# 커밋 템플릿 설정
git config commit.template .gitmessage
```

커밋 메시지 형식:
```
<타입>: <제목>

<본문>

<푸터>
```

**타입 종류**:
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포매팅
- `refactor`: 코드 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드 프로세스 또는 도구 변경

---

## 🤝 기여 방법

1. Feature 브랜치 생성 (`git checkout -b feature/amazing-feature`)
2. 변경 사항 커밋 (`git commit -m 'feat: Add amazing feature'`)
3. 브랜치에 Push (`git push origin feature/amazing-feature`)
4. Pull Request 생성

---

## 📄 라이선스

이 템플릿은 자유롭게 사용, 수정 및 배포할 수 있습니다.

---

## 🙋 도움말

문제가 발생하거나 질문이 있으면 이슈를 생성해 주세요.

**Happy Coding! 🚀**
