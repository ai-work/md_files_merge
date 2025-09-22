"""Markdown merging utilities."""

from .merger import (
    DEFAULT_DELIMITER,
    DEFAULT_HEADING_LEVEL,
    merge_markdown_files,
)

__all__ = [
    "merge_markdown_files",
    "DEFAULT_DELIMITER",
    "DEFAULT_HEADING_LEVEL",
]
