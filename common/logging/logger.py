"""
Logging module
Based on decompiled analysis
"""

import sys
from typing import Any, Optional
from contextlib import contextmanager


def log_debug(msg: str, *args: Any) -> None:
    """Log debug message"""
    if args:
        msg = msg % args
    print(f"[DEBUG] {msg}", file=sys.stderr)


def log_info(msg: str, *args: Any) -> None:
    """Log info message"""
    if args:
        msg = msg % args
    print(f"[INFO] {msg}", file=sys.stderr)


def log_warning(msg: str, *args: Any) -> None:
    """Log warning message"""
    if args:
        msg = msg % args
    print(f"[WARNING] {msg}", file=sys.stderr)


def log_error(msg: str, *args: Any) -> None:
    """Log error message"""
    if args:
        msg = msg % args
    print(f"[ERROR] {msg}", file=sys.stderr)


@contextmanager
def log_info_wrap(operation: str):
    """Context manager for logging operation start/end"""
    log_info(f"Starting {operation} operation...")
    try:
        yield
        log_info(f"Completed {operation} operation successfully.")
    except Exception as e:
        log_warning(f"{operation} operation failed: {e}")
        raise


class QuietError(Exception):
    """Silent error, no stack trace"""
    pass