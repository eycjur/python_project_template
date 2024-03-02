import json
import logging


class CloudLoggingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "severity": record.levelname,
            "message": f"[Application Log] {record.getMessage()}",
            # ミリ秒は直接利用することができない
            "time": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "logger": record.name,
            "trace": record.trace_id if hasattr(record, "trace_id") else None,
            "span": record.span_id if hasattr(record, "span_id") else None,
            "logging.googleapis.com/sourceLocation": {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            },
            "stack_trace": record.stack_info,
        }

        return json.dumps(log_data)
