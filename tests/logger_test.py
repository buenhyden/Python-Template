import logging
from unittest.mock import MagicMock, patch

import pytest

from src.core.logger import AppLogger


@pytest.fixture
def app_logger():
    return AppLogger(logger_name="test_logger")


def test_logger_initialization(app_logger):
    assert app_logger.logger.name == "test_logger"
    assert app_logger.logger.level == logging.INFO
    # Check if TraceIdFilter is added
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


def test_setup_file_logging(app_logger):
    # Mock os.makedirs and RotatingFileHandler
    with (
        patch("src.core.logger.RotatingFileHandler") as mock_handler,
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
        args, _ = mock_handler.call_args
        assert args[0] == "logs/app.log"

        handlers = logger.handlers
        assert len(handlers) > 0


def test_setup_custom_file_path(app_logger):
    custom_path = "custom_logs/custom.log"
    with (
        patch("src.core.logger.RotatingFileHandler") as mock_handler,
        patch("os.makedirs") as mock_makedirs,
    ):
        logger = app_logger.setup(
            service_name="test_service",
            enable_console=False,
            enable_file=True,
            enable_loki=False,
            log_file_path=custom_path,
        )

        mock_makedirs.assert_called_with("custom_logs", exist_ok=True)
        mock_handler.assert_called()
        args, _ = mock_handler.call_args
        assert args[0] == custom_path

        handlers = logger.handlers
        assert len(handlers) > 0


def test_setup_loki_logging(app_logger):
    fake_url = "http://mock-loki-url:3100"
    with patch("src.core.logger.LokiHandler") as mock_loki:
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


def test_trace_id_filter(app_logger):
    # Mock opentelemetry trace
    with patch("src.core.logger.trace") as mock_trace:
        mock_span = MagicMock()
        mock_span.get_span_context.return_value.trace_id = 0x1234567890ABCDEF1234567890ABCDEF
        mock_trace.get_current_span.return_value = mock_span

        record = logging.LogRecord(
            "name", logging.INFO, "pathname", 1, "msg", args=(), exc_info=None
        )

        trace_filter = AppLogger._TraceIdFilter()
        trace_filter.filter(record)

        assert record.trace_id == "1234567890abcdef1234567890abcdef"


def test_trace_id_filter_no_span(app_logger):
    with patch("src.core.logger.trace") as mock_trace:
        mock_trace.get_current_span.return_value = None

        record = logging.LogRecord(
            "name", logging.INFO, "pathname", 1, "msg", args=(), exc_info=None
        )

        trace_filter = AppLogger._TraceIdFilter()
        trace_filter.filter(record)

        assert record.trace_id == "0"
