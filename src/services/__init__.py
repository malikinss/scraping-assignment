# ./src/services/__init__.py

"""
This package contains the services used by the application.
"""

from .input_loader import URLInputLoader, URL, URLs
from .content_detector import ContentDetector, detector
from .metrics import MetricsCalculator, MetricsAggregator, MetricsSummary
from .result_manager import ResultManager

__all__ = [
    "URL",
    "URLs",
    "URLInputLoader",
    "ContentDetector",
    "detector",
    "MetricsCalculator",
    "MetricsAggregator",
    "MetricsSummary",
    "ResultManager"
]
