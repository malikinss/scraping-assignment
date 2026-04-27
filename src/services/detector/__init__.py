# ./src/services/detector/__init__.py
from .content_detector import ContentDetector
detector = ContentDetector()
__all__ = ["detector"]
