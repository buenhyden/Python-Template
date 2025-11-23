# 🐍 Python Template

FastAPI, Poetry, Docker를 사용하는 모던 Python 프로젝트 템플릿입니다.
확장 가능하고 유지보수가 용이한 백엔드 시스템을 구축하기 위한 견고한 기반을 제공합니다.

---

## ✨ 주요 기능 (Key Features)

- **🚀 FastAPI**: API 구축을 위한 고성능 비동기 웹 프레임워크.
- **📦 Poetry**: 의존성 관리 및 패키징을 위한 현대적인 도구.
- **🐳 Docker**: 일관된 개발 및 배포 환경을 위한 컨테이너화 지원.
- **⚡ Ruff**: 매우 빠른 Python 린터 및 코드 포매터.
- **🔒 Pre-commit**: 코드 품질 보장을 위한 자동화된 Git hooks.
- **✅ Pytest**: 신뢰성 있는 코드 작성을 위한 강력한 테스트 프레임워크.

---

## 📋 필수 요구 사항 (Prerequisites)

이 프로젝트를 실행하기 위해 다음 도구들이 필요합니다:

- **Python** 3.12 이상
- **Docker** 및 **Docker Compose**
- **Poetry**

---

## 🛠️ 설치 방법 (Installation)

### 1. 로컬 개발 환경 설정

**저장소 클론:**

```bash
git clone <repository-url>
cd python-template
```

**Poetry를 사용하여 의존성 설치:**

```bash
poetry install
```

**가상 환경 활성화:**

```bash
poetry shell
```

**Pre-commit hooks 설치:**

```bash
pre-commit install
```

### 2. Git 설정 (Git Setup)

일관된 커밋 메시지 작성을 위해 git commit 템플릿을 설정합니다:

```bash
git config commit.template .gitmessage
```

### 3. Pre-commit Hooks

이 프로젝트는 코드 품질을 보장하기 위해 `pre-commit`을 사용합니다.

**Pre-commit 설치:**

```bash
poetry add --group dev pre-commit
# 또는
pip install pre-commit
```

**Git hooks 설치:**

```bash
pre-commit install
```

**수동 실행 (선택 사항):**

```bash
pre-commit run --all-files
```

### 4. Docker 설정

**컨테이너 빌드 및 실행:**

```bash
docker-compose up --build
```

---

## 🚀 사용 방법 (Usage)

### 애플리케이션 실행

**로컬에서 실행:**

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Docker로 실행:**

애플리케이션은 `http://localhost:8000`에서 접근할 수 있습니다.

### 📚 API 문서 (API Documentation)

애플리케이션이 실행되면 다음 주소에서 대화형 API 문서를 확인할 수 있습니다:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 💻 개발 (Development)

### 테스트 실행

```bash
pytest
```

### 린팅 및 포매팅

Ruff를 실행하여 코드를 검사하고 포맷팅합니다:

```bash
ruff check .
ruff format .
```

---

## 📂 프로젝트 구조 (Project Structure)

```
.
├── .github/            # 🤖 GitHub Actions 워크플로우
├── deploy/             # 🚀 배포 설정
├── logs/               # 📝 애플리케이션 로그
├── src/                # 🧠 소스 코드
│   ├── core/           # ⚙️ 핵심 기능 (설정, 로거)
│   ├── db/             # 💾 데이터베이스 관련 코드
│   ├── main.py         # 🏁 애플리케이션 진입점
│   └── ...
├── tests/              # 🧪 테스트 코드
├── Dockerfile          # 🐳 Docker 설정
├── docker-compose.yml  # 🐙 Docker Compose 설정
├── pyproject.toml      # 📦 Poetry 설정
├── .gitmessage         # 📝 Git 커밋 템플릿
├── .pre-commit-config.yaml # 🔒 Pre-commit 설정
└── README.md           # 📖 프로젝트 문서
```
