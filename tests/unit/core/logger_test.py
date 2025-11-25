import logging
import uuid
from unittest.mock import MagicMock, patch

import pytest

from src.core.logger import AppLogger


@pytest.fixture
def app_logger():
    unique_name = f"test_logger_{uuid.uuid4().hex}"
    return AppLogger(logger_name=unique_name)


def test_logger_initialization(app_logger):
    assert "test_logger_" in app_logger.logger.name
    assert app_logger.logger.level == logging.INFO

    # Logger에 직접 부착된 필터 확인
    filters = [f for f in app_logger.logger.filters if isinstance(f, AppLogger._TraceIdFilter)]
    assert len(filters) > 0


def test_setup_console_logging(app_logger):
    logger = app_logger.setup(
        service_name="test_service",
        enable_console=True,
        enable_file=False,
        enable_loki=False,
    )

    handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
    assert len(handlers) >= 1

    # 핸들러에도 필터가 잘 붙었는지 확인
    assert any(isinstance(f, AppLogger._TraceIdFilter) for f in handlers[0].filters)


def test_setup_file_logging(app_logger):
    # patch를 사용하여 파일 시스템 접근을 차단합니다.
    with (
        patch("src.core.logger.app_logger.RotatingFileHandler") as mock_handler,
        patch("os.makedirs") as mock_makedirs,
    ):
        logger = app_logger.setup(
            service_name="test_service",
            enable_console=False,
            enable_file=True,
            enable_loki=False,
        )

        mock_makedirs.assert_called_with("logs", exist_ok=True)
        mock_handler.assert_called()

        # 생성된 로거에 핸들러가 있는지 확인 (Mock 핸들러가 들어감)
        assert len(logger.handlers) > 0


def test_setup_custom_file_path(app_logger):
    custom_path = "custom_logs/custom.log"
    with (
        patch("src.core.logger.app_logger.RotatingFileHandler") as mock_handler,
        patch("os.makedirs") as mock_makedirs,
    ):
        app_logger.setup(
            service_name="test_service",
            enable_console=False,
            enable_file=True,
            enable_loki=False,
            log_file_path=custom_path,
        )

        mock_makedirs.assert_called_with("custom_logs", exist_ok=True)
        # 호출 인자 확인 (args[0]가 경로)
        args, _ = mock_handler.call_args
        assert args[0] == custom_path


def test_setup_loki_logging(app_logger):
    fake_url = "http://mock-loki-url:3100"
    # LokiHandler가 설치되지 않았을 수도 있으므로 조건부 Patch
    with patch("src.core.logger.app_logger.LokiHandler", create=True) as mock_loki:
        logger = app_logger.setup(
            service_name="test_service",
            loki_url=fake_url,
            enable_console=False,
            enable_file=False,
            enable_loki=True,
        )

        mock_loki.assert_called_with(
            url=fake_url, tags={"application": "test_service"}, version="1"
        )
        assert len(logger.handlers) > 0


def test_trace_id_filter_logic():
    """
    AppLogger 인스턴스 생성 없이 필터 로직만 독립적으로 검증합니다.
    """
    # Mock Span Context
    mock_span = MagicMock()
    # Trace ID는 128비트 정수입니다.
    mock_span.get_span_context.return_value.trace_id = 0x1234567890ABCDEF1234567890ABCDEF

    # OpenTelemetry의 trace 모듈을 Mocking
    with patch("src.core.logger.app_logger.trace") as mock_trace:
        mock_trace.get_current_span.return_value = mock_span
        # INVALID_SPAN_CONTEXT 비교를 위해 Mock 설정
        mock_trace.INVALID_SPAN_CONTEXT = MagicMock()

        # 로그 레코드 생성
        record = logging.LogRecord(
            "test_logger", logging.INFO, "test.py", 1, "test message", args=(), exc_info=None
        )

        # 필터 실행
        trace_filter = AppLogger._TraceIdFilter()
        trace_filter.filter(record)

        # 기대값: 소문자 32자리 16진수
        expected_trace_id = "1234567890abcdef1234567890abcdef"
        assert record.trace_id == expected_trace_id  # type: ignore[attr-defined]


def test_trace_id_filter_no_span():
    """Span이 없을 때 기본값 0이 설정되는지 확인"""
    with patch("src.core.logger.app_logger.trace") as mock_trace:
        mock_trace.get_current_span.return_value = None

        record = logging.LogRecord(
            "test_logger", logging.INFO, "test.py", 1, "msg", args=(), exc_info=None
        )

        trace_filter = AppLogger._TraceIdFilter()
        trace_filter.filter(record)

        assert record.trace_id == "0"  # type: ignore[attr-defined]
