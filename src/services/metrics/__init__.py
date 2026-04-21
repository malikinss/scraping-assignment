# ./src/services/metrics/__init__.py

"""
Metrics Service Package
=======================

This module is responsible for metrics for the scraping process.
It is used to group all the necessary imports for the metrics service.

Key Features:
    - Pipeline-based metrics calculation
    - Rate calculation
    - Latency calculation
    - Content length calculation

Usage:
    >>> from src.services.metrics import MetricsAggregator
    >>> aggregator = MetricsAggregator()
    >>> metrics = aggregator.metrics(results)
    >>> print(metrics)
"""

from .models import MetricsSummary
from .reporter import MetricsReporter
from .calculator import MetricsCalculator
from .aggregator import MetricsAggregator

__all__ = [
    "MetricsSummary",
    "MetricsCalculator",
    "MetricsReporter",
    "MetricsAggregator"
]
