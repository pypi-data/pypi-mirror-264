import logging
from json import dumps
from time import time_ns
from typing import Any

from aiohttp.abc import AbstractAccessLogger
from aiohttp.web import BaseRequest, StreamResponse

from alxhttp.req_id import get_request_id

_compact_separators = (",", ":")

try:
    from aws_xray_sdk.core import xray_recorder
except ImportError:
    xray_recorder = None
    pass


def compact_json(obj: Any) -> str:
    return dumps(
        obj,
        indent=None,
        ensure_ascii=True,
        separators=_compact_separators,
    )


class JSONAccessLogger(AbstractAccessLogger):
    def __init__(self, logger: logging.Logger, log_format: str):
        super().__init__(logger, log_format)

    def log(
        self,
        request: BaseRequest,
        response: StreamResponse,
        time: float,
    ) -> None:
        """
        Taking some naming conventions from:
        https://github.com/opentracing/specification/blob/master/semantic_conventions.md
        """

        trace_id = None
        if xray_recorder is not None:
            try:
                trace = xray_recorder.get_trace_entity()
                if trace and trace.trace_id:
                    trace_id = trace.trace_id
            except Exception:
                pass
            # record.__dict__.update(traceId=trace.trace_id)

        request_id = get_request_id(request)

        self.logger.info(
            compact_json(
                {
                    "message": f"{request.method} {request.url.path} {response.status}",
                    "duration": round(time, 8),
                    "time_ns": time_ns(),
                    "http": {
                        "method": request.method,
                        "status_code": response.status,
                        "url": str(request.url),
                    },
                    "component": "aiohttp",
                    "request_id": request_id,
                    "traceId": trace_id,
                }
            )
        )
