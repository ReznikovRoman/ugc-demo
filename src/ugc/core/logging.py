from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from logstash import LogstashHandler
from loguru import logger

from ugc.common.constants import ELK_TAG

if TYPE_CHECKING:
    from loguru import Logger, Record


def init_logstash_handler(host: str, port: int, version: int) -> LogstashHandler:
    logstash_handler = LogstashHandler(host=host, port=port, version=version)
    yield logstash_handler


def init_logger(handler: logging.Handler, log_format: str, level: str | int) -> Logger:
    logger.add(
        handler,
        format=log_format,
        level=level,
        filter=custom_fields_filter,
    )
    yield logger


def custom_fields_filter(record: Record) -> bool:
    """Добавление дополнительных полей к записи в лог."""
    extra_fields = record.get("extra")
    request_id = extra_fields.get("request_id")
    record["request_id"] = request_id
    record["tag"] = ELK_TAG
    return True
