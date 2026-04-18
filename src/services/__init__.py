# ./src/services/__init__.py

"""
Package `services`
================

This package contains the application services, which are reusable components
that provide specific functionality to the application. These services are
organized into subpackages, each with its own responsibilities.

Subpackages:
    - result_manager: Manages and persists scraping results.
    - input_loader: Loads URLs from different sources.
    - content_detector: Detects the content type of a URL.
    - metrics: Calculates and reports metrics.

Imports:
    URL: Type alias for URL string.
    URLs: Type alias for list of URL strings.
    URLInputLoader: Service for loading URLs from different sources.
    detector: Service for detecting the content type of a URL.
    MetricsCalculator: Service for calculating metrics.
    MetricsSummary: Service for summarizing metrics.
    MetricsReporter: Service for reporting metrics.
    ResultManager: Service for managing and persisting results.

Usage:
    >>> from src.services import URLInputLoader, MetricsCalculator,
    ...     MetricsSummary, MetricsReporter, ResultManager, detector
    >>> loader = URLInputLoader()
    >>> metrics_calculator = MetricsCalculator()
    >>> metrics_summary = MetricsSummary()
    >>> metrics_reporter = MetricsReporter()
    >>> result_manager = ResultManager("results.csv")
    >>> detector = detector.detect()
"""
from .content_detector import detector
from .input_loader import URLInputLoader
from .result_manager import ResultManager
from .metrics import MetricsCalculator, MetricsSummary, MetricsReporter

__all__ = [
    detector,
    ResultManager,
    URLInputLoader,
    MetricsCalculator,
    MetricsSummary,
    MetricsReporter
]
