# Logging prometheus

Poetry plugin to set package version based on git tag.

[![PyPI](https://img.shields.io/pypi/v/logs-prometheus)](https://pypi.org/project/logs-prometheus/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/logs-prometheus)](https://pypi.org/project/logs-prometheus/)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/logs-prometheus)](https://gitlab.com/rocshers/python/logs-prometheus)
[![Docs](https://img.shields.io/badge/docs-exist-blue)](https://rocshers.gitlab.io/python/logs-prometheus/)

[![Test coverage](https://codecov.io/gitlab/rocshers:python/logs-prometheus/graph/badge.svg?token=3C6SLDPHUC)](https://codecov.io/gitlab/rocshers:python/logs-prometheus)
[![Downloads](https://static.pepy.tech/badge/logs-prometheus)](https://pepy.tech/project/logs-prometheus)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/logs-prometheus)](https://gitlab.com/rocshers/python/logs-prometheus)

## Functionality

- Logs **handler**, creating metrics
- Setup **labels**

![example](https://gitlab.com/rocshers/python/logs-prometheus/-/raw/main/docs/grafana_example.png)

## Quick start

install:

```bash
pip install logs-prometheus
```

usage:

```python
import logging

from logging_prometheus.handlers import PrometheusHandler

logger = logging.getLogger()
logger.addHandler(PrometheusHandler('python_logging_', ['name', 'levelname', 'module']))
# or
# from logging_prometheus import setup_prometheus_handler_for_root
# setup_prometheus_handler_for_root()

logger = logging.getLogger('app')

logger.debug('debug')
logger.info('info')
logger.warning('warning')
logger.error('error')
```

## Django setup

```python
LOGGING = {
    ...
    "handlers": {
        "prometheus": {
            "class": "logging_prometheus.PrometheusHandler",
            "prefix": "python_logging_",
            "labels": ["name", "levelname", "module"],
        },
        ...
    },
    "loggers": {
        "django": {
            "handlers": ["prometheus", ...],
            "level": "DEBUG",
            "propagate": True,
        },
        ...
    },
    ...
}
```

## Labels

The handler supports `all values` that are in the log object. more details: <https://docs.python.org/3/library/logging.html#logging.LogRecord>

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/logs-prometheus/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/logs-prometheus>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
