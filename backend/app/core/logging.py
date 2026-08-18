import logging
import sys
from typing import Any


class StructuredLogger:
    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message: str, **kwargs: Any) -> None:
        self.logger.info("%s %s", message, self._format_kwargs(kwargs))

    def warning(self, message: str, **kwargs: Any) -> None:
        self.logger.warning("%s %s", message, self._format_kwargs(kwargs))

    def error(self, message: str, **kwargs: Any) -> None:
        self.logger.error("%s %s", message, self._format_kwargs(kwargs))

    @staticmethod
    def _format_kwargs(kwargs: dict[str, Any]) -> str:
        return " ".join(f"{key}={value}" for key, value in sorted(kwargs.items()))


def get_logger(name: str) -> StructuredLogger:
    return StructuredLogger(name)
