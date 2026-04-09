# ./src/services/metrics/__init__.py

"""
Metrics package

Contains classes and utilities to calculate, summarize,
and report scraping metrics.

Exports:
    - MetricsSummary: Dataclass holding aggregated metrics.
    - MetricsCalculator: Computes metrics from scrape results.
    - MetricsReporter: Formats and outputs metrics.
"""

from .models import MetricsSummary
from .calculator import MetricsCalculator
from .reporter import MetricsReporter

__all__ = ["MetricsSummary", "MetricsCalculator", "MetricsReporter"]
