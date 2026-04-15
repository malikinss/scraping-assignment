# ./src/logger/log_parts.py

"""
Reusable log message components and format helpers.

This module provides a collection of utility methods for constructing
structured log message parts in a consistent format.

It standardizes:
    - Key-value formatting (e.g., key=value)
    - Bracketed segments (e.g., [INFO], [ID:1])
    - Common fields (latency, status, url, etc.)
    - Formatting helpers for time and counts

The goal is to ensure consistency and readability across all logging
output in the application.
"""

from .deps import URLUtils, Optional


class LogParts:
    """
    Utility class for building structured log message fragments.

    Provides reusable formatting methods to compose log messages in a
    consistent and readable way across different modules.

    All methods are class/static methods to allow stateless usage.
    """
    @classmethod
    def bracket(cls, text: str) -> str:
        """
        Wrap text in square brackets.

        Args:
            text (str): Text to wrap.

        Returns:
            str: Formatted string in brackets.
        """
        return f"[{text}]"

    @classmethod
    def kv(cls, key: str, value: str) -> str:
        """
        Format as key-value pair.

        Args:
            key (str): Key name.
            value (str): Value.

        Returns:
            str: Formatted key-value string.
        """
        return f"{key}={value}"

    @classmethod
    def upper(cls, text: str) -> str:
        """
        Convert text to uppercase.

        Args:
            text (str): Text to convert.

        Returns:
            str: Uppercase text.
        """
        return text.upper()

    @classmethod
    def id(cls, id: int) -> str:
        """
        Format ID in bracket notation.

        Args:
            id (int): ID value.

        Returns:
            str: Formatted ID string.
        """
        return cls.bracket(f"ID:{id}")

    @classmethod
    def method(cls, method: str) -> str:
        """
        Format HTTP method in bracket notation.

        Args:
            method (str): HTTP method.

        Returns:
            str: Formatted method string.
        """
        return cls.bracket(cls.upper(method))

    @classmethod
    def status(cls, status: str) -> str:
        """
        Format HTTP status in bracket notation.

        Args:
            status (str): HTTP status.

        Returns:
            str: Formatted status string.
        """
        return cls.bracket(cls.upper(status))

    @classmethod
    def latency(cls, latency: float) -> str:
        """
        Format latency in seconds.

        Args:
            latency (float): Latency in seconds.

        Returns:
            str: Formatted latency string.
        """
        return cls.kv("latency", f"{latency:.3f}s")

    @classmethod
    def content_length(cls, content_length: int) -> str:
        """
        Format content length.

        Args:
            content_length (int): Content length.

        Returns:
            str: Formatted content length string.
        """
        return cls.kv("content_length", content_length)

    @classmethod
    def error(cls, error: Optional[str]) -> str:
        """
        Format error message.

        Args:
            error (Optional[str]): Error message.

        Returns:
            str: Formatted error string.
        """
        return cls.kv("error", error or "N/A")

    @classmethod
    def url(cls, url) -> str:
        """
        Format URL.

        Args:
            url: URL to format.

        Returns:
            str: Formatted URL string.
        """
        return cls.kv("url", URLUtils.short_url(url))

    @classmethod
    def timeout(cls, timeout: float) -> str:
        """
        Format timeout in seconds.

        Args:
            timeout (float): Timeout in seconds.

        Returns:
            str: Formatted timeout string.
        """
        return cls.kv("timeout", cls.seconds(timeout))

    @staticmethod
    def attempt(
        attempt: Optional[int],
        retries: Optional[int]
    ) -> str:
        """
        Format attempt information.

        Args:
            attempt (Optional[int]): Attempt number.
            retries (Optional[int]): Total retries.

        Returns:
            str: Formatted attempt string.
        """
        if attempt is None:
            return ""
        return f" (attempt {attempt}/{retries}) "

    @classmethod
    def concurrency(cls, concurrency: int) -> str:
        """
        Format concurrency level.

        Args:
            concurrency (int): Concurrency level.

        Returns:
            str: Formatted concurrency string.
        """
        return cls.kv("concurrency", concurrency)

    @classmethod
    def total(cls, total: int) -> str:
        """
        Format total count.

        Args:
            total (int): Total count.

        Returns:
            str: Formatted total string.
        """
        return cls.kv("total", total)

    @classmethod
    def reason(cls, reason: str) -> str:
        """
        Format reason.

        Args:
            reason (str): Reason.

        Returns:
            str: Formatted reason string.
        """
        return cls.kv("reason", reason)

    @classmethod
    def success(cls, success: int, total: int) -> str:
        """
        Format success count.

        Args:
            success (int): Success count.
            total (int): Total count.

        Returns:
            str: Formatted success string.
        """
        return cls.kv("success", f"{success}/{total}")

    @classmethod
    def target(cls, target: str) -> str:
        """
        Format target.

        Args:
            target (str): Target.

        Returns:
            str: Formatted target string.
        """
        return cls.kv("target", target)

    @classmethod
    def details(cls, details: dict) -> str:
        """
        Format details.

        Args:
            details (dict): Details.

        Returns:
            str: Formatted details string.
        """
        return cls.kv("details", details)

    @classmethod
    def retries(cls, retries: int) -> str:
        """
        Format retries.

        Args:
            retries (int): Retries.

        Returns:
            str: Formatted retries string.
        """
        return cls.kv("retries", retries)

    @classmethod
    def http_timeout(cls, http_timeout: float) -> str:
        """
        Format HTTP timeout.

        Args:
            http_timeout (float): HTTP timeout.

        Returns:
            str: Formatted HTTP timeout string.
        """
        return cls.kv("http_timeout", cls.seconds(http_timeout))

    @classmethod
    def browser_timeout(cls, browser_timeout: float) -> str:
        """
        Format browser timeout.

        Args:
            browser_timeout (float): Browser timeout.

        Returns:
            str: Formatted browser timeout string.
        """
        return cls.kv("browser_timeout", cls.milliseconds(browser_timeout))

    @classmethod
    def source(cls, source: str) -> str:
        """
        Format source.

        Args:
            source (str): Source.

        Returns:
            str: Formatted source string.
        """
        return cls.kv("source", source)

    @classmethod
    def hostname(cls, hostname: str) -> str:
        """
        Format hostname.

        Args:
            hostname (str): Hostname.

        Returns:
            str: Formatted hostname string.
        """
        return cls.kv("hostname", hostname)

    @classmethod
    def path(cls, path: str) -> str:
        """
        Format path.

        Args:
            path (str): Path.

        Returns:
            str: Formatted path string.
        """
        return cls.kv("path", path)

    @classmethod
    def duplicates_removed(cls, duplicates: int) -> str:
        """
        Format duplicates removed.

        Args:
            duplicates (int): Duplicates removed.

        Returns:
            str: Formatted duplicates removed string.
        """
        return cls.kv("duplicates_removed", duplicates)

    @classmethod
    def invalid(cls, invalid: int) -> str:
        """
        Format invalid.

        Args:
            invalid (int): Invalid.

        Returns:
            str: Formatted invalid string.
        """
        return cls.kv("invalid", invalid)

    @classmethod
    def valid(cls, valid: int) -> str:
        """
        Format valid.

        Args:
            valid (int): Valid.

        Returns:
            str: Formatted valid string.
        """
        return cls.kv("valid", valid)

    @classmethod
    def count(cls, count: int) -> str:
        """
        Format count.

        Args:
            count (int): Count.

        Returns:
            str: Formatted count string.
        """
        return cls.kv("count", count)

    @staticmethod
    def seconds(value: float) -> str:
        """
        Format seconds.

        Args:
            value (float): Seconds.

        Returns:
            str: Formatted seconds string.
        """
        return f"{value:.3f}s"

    @staticmethod
    def milliseconds(value: float) -> str:
        """
        Format milliseconds.

        Args:
            value (float): Milliseconds.

        Returns:
            str: Formatted milliseconds string.
        """
        return f"{value:.0f}ms"

    @classmethod
    def name(cls, name: str) -> str:
        """
        Format name.

        Args:
            name (str): Name.

        Returns:
            str: Formatted name string.
        """
        return cls.bracket(cls.upper(name))

    @classmethod
    def title(cls, name: str, title: str) -> str:
        """
        Format title.

        Args:
            name (str): Name.
            title (str): Title.

        Returns:
            str: Formatted title string.
        """
        return f"{cls.name(name)} {title}"

    @classmethod
    def prefix(cls, id: int, method: str, url, timeout: float):
        """
        Format prefix.

        Args:
            id (int): ID.
            method (str): Method.
            url: URL.
            timeout (float): Timeout.

        Returns:
            str: Formatted prefix string.
        """
        return (
            f"{cls.id(id)} "
            f"{cls.method(method)} "
            f"{cls.url(url)} "
            f"{cls.timeout(timeout)}"
        )

    @staticmethod
    def pipeline_terminated(reason: str) -> str:
        """
        Format pipeline terminated.

        Args:
            reason (str): Reason.

        Returns:
            str: Formatted pipeline terminated string.
        """
        return f"Pipeline terminated: {reason}"
