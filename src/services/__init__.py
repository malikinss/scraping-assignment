# ./src/services/__init__.py

"""
This package contains the services used by the application.
"""

from .result_manager import ResultManager
from .input_loader import URLInputLoader, URL, URLs
from .content_detector import ContentDetector, detector
from .metrics import (
    MetricsCalculator,
    MetricsAggregator,
    MetricsSummary,
    MetricsReporter
)


__all__ = [
    "URL",
    "URLs",
    "URLInputLoader",
    "ContentDetector",
    "detector",
    "MetricsCalculator",
    "MetricsAggregator",
    "MetricsSummary",
    "MetricsReporter",
    "ResultManager"
]
