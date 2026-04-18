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
    >>> from src.services.metrics import MetricsCalculator
    >>> calculator = MetricsCalculator()
    >>> metrics = calculator.calculate(results)
    >>> print(metrics)

Example:
    >>> from src.services.metrics import MetricsCalculator
    >>> calculator = MetricsCalculator()
    >>> metrics = calculator.calculate(results)
    >>> print(metrics)
"""

from .models import MetricsSummary
from .calculator import MetricsCalculator
from .reporter import MetricsReporter

__all__ = ["MetricsSummary", "MetricsCalculator", "MetricsReporter"]
