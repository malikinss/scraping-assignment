# ./src/models/common.py

"""
Shared type definitions for core scraping domain models.

This module defines common type aliases used across the scraping system,
including URL representations and aggregated metrics structures.

These types improve type safety and readability by providing semantic
aliases over built-in Python types.
"""

from .enums import ScrapeStatus
from .deps import List, NewType, Dict

URL = NewType("URL", str)
"""
Type alias representing a validated URL string.

This is a semantic wrapper over `str` used to improve type clarity
and distinguish URLs from arbitrary strings.
"""

URLs = List[URL]
"""
List of URL values used as input for scraping pipelines.
"""

Counts = Dict[ScrapeStatus, int]
"""
Dictionary mapping scrape statuses to their occurrence counts.

Used for aggregating pipeline results (success, failed, timeout, etc.).
"""
