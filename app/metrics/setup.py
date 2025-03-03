from fastapi import FastAPI
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.trace import set_tracer_provider
from prometheus_client import start_http_server

from app.metrics.hooks import client_response_hook


__all__ = ["setup_metrics"]


def setup_metrics(app: FastAPI, port: int = 9200, address: str = "0.0.0.0") -> None:
    resource = Resource(
        attributes={"service.name": app.title, "service.version": app.version}  # noqa
    )
    reader = PrometheusMetricReader()
    start_http_server(port=port, addr=address)
    tracer_provider = TracerProvider(resource=resource)
    provider = MeterProvider(metric_readers=[reader], resource=resource)
    set_meter_provider(meter_provider=provider)
    set_tracer_provider(tracer_provider=tracer_provider)
    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=tracer_provider,
        meter_provider=provider,
        client_response_hook=client_response_hook,
        excluded_urls="docs,redoc,openapi.json",
    )
