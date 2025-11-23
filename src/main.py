from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# OpenTelemetry 관련 임포트
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from contextlib import asynccontextmanager

from src.core.config import settings
from src.core.logger import app_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Logger is already setup at module level
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# ---------------------------------------------------------
# A. Tempo (Tracing) 설정
# ---------------------------------------------------------
# 서비스 이름 설정 (Grafana에서 이 이름으로 찾음)
resource = Resource(attributes={"service.name": settings.PROJECT_NAME})

# Trace Provider 설정
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
# Exporter 설정 (Docker의 Tempo gRPC 포트 4317로 전송)
# 로컬 실행 시: localhost, Docker 내부 실행 시: tempo
otlp_exporter = OTLPSpanExporter(endpoint=settings.TEMPO_EXPORTER, insecure=True)

# Span을 배치로 모아서 전송 (성능 최적화)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# FastAPI 자동 계측 (HTTP 요청 들어오면 자동으로 Trace 시작)
FastAPIInstrumentor.instrument_app(app)

# ---------------------------------------------------------
# Logging 설정
# ---------------------------------------------------------
logger = app_logger.setup(
    service_name=settings.PROJECT_NAME,
    loki_url=settings.LOKI_URL,
    enable_console=True,
    enable_file=True,
    enable_loki=True,
)

# ---------------------------------------------------------
# CORS 설정 (React 앱 연동)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 환경에서는 구체적인 도메인으로 변경 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"Hello": "World"}
