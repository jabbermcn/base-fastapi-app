from opentelemetry.sdk.trace import Span
from prometheus_client import Counter


__all__ = ["client_response_hook"]


class ClientResponseHook:
    HTTP_REQUESTS_TOTAL_COUNTER = Counter(
        name="http_requests_total",
        documentation="Total number of requests by method, status and handler.",
        labelnames=(
            "handler",
            "method",
            "status",
        ),
    )

    def __call__(self, span: Span, scope: dict, message: dict) -> None:
        self.http_requests_total(span=span, scope=scope, message=message)

    def http_requests_total(self, span: Span, scope: dict, message: dict) -> None:
        if message.get("type") == "http.response.start":
            self.HTTP_REQUESTS_TOTAL_COUNTER.labels(scope.get("path"), scope.get("method"), message.get("status")).inc()


client_response_hook = ClientResponseHook()
