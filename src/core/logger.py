import logging
import sys
import os
from typing import Optional
from logging.handlers import RotatingFileHandler
from logging_loki import LokiHandler
from opentelemetry import trace


class AppLogger:
    def __init__(self, logger_name: str = "uvicorn"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)

    class _TraceIdFilter(logging.Filter):
        def filter(self, record):
            span = trace.get_current_span()
            if span:
                trace_id = span.get_span_context().trace_id
                if trace_id:
                    record.trace_id = format(trace_id, "032x")
                else:
                    record.trace_id = "0"
            else:
                record.trace_id = "0"
            return True

    def setup(
        self,
        service_name: str,
        loki_url: Optional[str] = None,
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

        # Clear existing handlers to avoid duplicates if setup is called multiple times
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 공통 필터 인스턴스 하나 생성
        trace_filter = self._TraceIdFilter()
        self.logger.addFilter(trace_filter)

        # 1. Console Handler
        if enable_console:
            console_handler = logging.StreamHandler(sys.stderr)
            # Use uvicorn's default formatter if available, else standard
            try:
                from uvicorn.logging import DefaultFormatter

                formatter = DefaultFormatter(
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
            formatter = logging.Formatter(
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
