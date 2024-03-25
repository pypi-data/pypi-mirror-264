import logging

from logging_prometheus.handlers import PrometheusHandler


def setup_prometheus_handler_for_root(*args, **kwargs):
    logger = logging.getLogger()
    logger.addHandler(PrometheusHandler(*args, **kwargs))
