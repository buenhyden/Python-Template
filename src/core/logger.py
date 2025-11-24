import logging
import os
import sys
from logging.handlers import RotatingFileHandler

# loki 라이브러리가 없을 경우를 대비한 처리 (선택사항)
try:
    from logging_loki import LokiHandler
except ImportError:
    LokiHandler = None

from opentelemetry import trace


class AppLogger:
    def __init__(self, logger_name: str = "uvicorn"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        if not any(isinstance(f, self._TraceIdFilter) for f in self.logger.filters):
            self.logger.addFilter(self._TraceIdFilter())

    class _TraceIdFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            span = trace.get_current_span()
            if span:
                span_context = span.get_span_context()
                if span_context != trace.INVALID_SPAN_CONTEXT:
                    record.trace_id = format(span_context.trace_id, "032x")  # type: ignore[attr-defined]
                else:
                    record.trace_id = "0"  # type: ignore[attr-defined]
            else:
                record.trace_id = "0"  # type: ignore[attr-defined]
            return True

    def setup(
        self,
        service_name: str,
        loki_url: str | None = None,
        enable_console: bool = True,
        enable_file: bool = True,
        enable_loki: bool = False,
        log_file_path: str = "logs/app.log",
    ) -> logging.Logger:
        """
        Setup and return the configured logger.

        Args:
            service_name: Name of the service for tagging.
            loki_url: URL for Loki (required if enable_loki is True).
            enable_console: Enable console logging (stderr).
            enable_file: Enable file logging.
            enable_loki: Enable Loki logging.
            log_file_path: Path to the log file (default: logs/app.log).
        """

        # 기존 핸들러 정리 (중복 방지)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 핸들러에 부착할 필터 인스턴스 생성
        trace_filter = self._TraceIdFilter()

        # 1. Console Handler
        if enable_console:
            console_handler = logging.StreamHandler(sys.stderr)
            # Use uvicorn's default formatter if available, else standard
            formatter: logging.Formatter
            try:
                from uvicorn.logging import DefaultFormatter

                formatter = DefaultFormatter(  # type: ignore[assignment]
                    "%(levelprefix)s | %(asctime)s | %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            except ImportError:
                formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )

            console_handler.setFormatter(formatter)
            console_handler.addFilter(trace_filter)  # ★ 여기 추가
            self.logger.addHandler(console_handler)

        # 2. File Handler
        if enable_file:
            log_dir = os.path.dirname(log_file_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding="utf-8",
            )
            formatter = logging.Formatter(  # type: ignore[assignment]
                "%(asctime)s - %(name)s - %(levelname)s - [TraceID: %(trace_id)s] - %(message)s"
            )
            file_handler.setFormatter(formatter)
            file_handler.addFilter(trace_filter)  # ★ 여기 추가
            self.logger.addHandler(file_handler)

        # 3. Loki Handler
        if enable_loki and loki_url:
            loki_handler = LokiHandler(
                url=loki_url,
                tags={"application": service_name},
                version="1",
            )
            loki_handler.addFilter(trace_filter)  # ★ 여기 추가
            self.logger.addHandler(loki_handler)
        elif enable_loki and not loki_url:
            print("Warning: Loki logging enabled but no URL provided.")

        return self.logger


# Singleton instance
app_logger = AppLogger()
