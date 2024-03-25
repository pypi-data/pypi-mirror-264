import logging
from typing import Dict, List

from prometheus_client import REGISTRY, CollectorRegistry, Counter

PROMETHEUS_LOG_COUNTERS: Dict[str, Counter] = {}


def get_counter(registry: CollectorRegistry, prefix: str, labels: List[str]) -> Counter:
    if prefix not in PROMETHEUS_LOG_COUNTERS:
        PROMETHEUS_LOG_COUNTERS[prefix] = Counter(
            f'{prefix}logs',
            'Count of log with labels',
            labels,
            registry=registry,
        )

    return PROMETHEUS_LOG_COUNTERS[prefix]


class PrometheusHandler(logging.Handler):
    """logging.Handler for creating prometheus metrics"""

    prefix: str

    def __init__(
        self,
        prefix: str = 'python_logging_',
        labels: List[str] = ['name', 'levelname'],
        registry: CollectorRegistry = REGISTRY,
    ) -> None:
        super().__init__()

        self.labels = labels
        self.counter = get_counter(registry, prefix, labels)

    def emit(self, record: logging.LogRecord):
        labels = {i: getattr(record, i) for i in self.labels}
        self.counter.labels(**labels).inc()
