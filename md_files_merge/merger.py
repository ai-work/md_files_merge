"""Utilities for merging Markdown files into a single document."""
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

DEFAULT_HEADING_LEVEL = 1
DEFAULT_DELIMITER = "<<<>>>"

MarkdownPathPair = Tuple[Path, Path]


def _validate_heading_level(level: int) -> int:
    if not 1 <= level <= 6:
        raise ValueError("heading_level must be between 1 and 6")
    return level


def _collect_markdown_files(root: Path, output: Path | None = None) -> List[MarkdownPathPair]:
    """Collect Markdown files under ``root``.

    Parameters
    ----------
    root:
        The directory whose Markdown files should be discovered.
    output:
        Optional path to the output file. If provided and the path is within
        ``root`` it will be skipped during collection to avoid self-inclusion.

    Returns
    -------
    list[tuple[pathlib.Path, pathlib.Path]]
        A list of tuples containing the absolute path to the Markdown file and
        its path relative to ``root``. Within each directory a ``README.md``
        file (matched case-insensitively) is returned before any other Markdown
        files.
    """

    markdown_files: List[MarkdownPathPair] = []
    resolved_output = output.resolve() if output is not None else None

    for directory, dirnames, filenames in os.walk(root):
        dirnames.sort()
        markdown_names = sorted(
            (name for name in filenames if name.lower().endswith(".md")),
            key=lambda name: (name.lower() != "readme.md", name.lower()),
        )
        for name in markdown_names:
            file_path = Path(directory) / name
            if resolved_output is not None and file_path.resolve() == resolved_output:
                continue
            markdown_files.append((file_path, file_path.relative_to(root)))

    return markdown_files


def merge_markdown_files(
    root: str | Path,
    output: str | Path,
    *,
    heading_level: int = DEFAULT_HEADING_LEVEL,
    delimiter: str = DEFAULT_DELIMITER,
) -> Path:
    """Merge Markdown files under ``root`` into a single document.

    The Markdown files are discovered recursively in alphabetical order (with
    ``README.md`` files given precedence within their directories) and their
    raw contents are appended sequentially into the output file. This function
    can be imported and used programmatically as part of larger workflows or
    invoked through the accompanying command line interface.

    Parameters
    ----------
    root:
        Directory to search for Markdown files.
    output:
        File path where the merged Markdown document will be written.
    heading_level:
        Retained for backwards compatibility. Previously controlled the
        heading level used between files but no longer has any effect.
    delimiter:
        Retained for backwards compatibility. Previously wrapped headings to
        avoid collisions with existing content but no longer has any effect.

    Returns
    -------
    pathlib.Path
        The path to the written Markdown file.
    """

    root_path = Path(root).expanduser().resolve()
    if not root_path.is_dir():
        raise ValueError(f"root path '{root}' does not exist or is not a directory")

    output_path = Path(output).expanduser().resolve()

    _validate_heading_level(heading_level)
    if not delimiter:
        raise ValueError("delimiter must be a non-empty string")

    markdown_files = _collect_markdown_files(root_path, output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as merged_file:
        for index, (file_path, _) in enumerate(markdown_files):
            if index:
                merged_file.write("\n\n")

            content = file_path.read_text(encoding="utf-8")
            merged_file.write(content.rstrip("\n"))

        if markdown_files:
            merged_file.write("\n")

    return output_path


__all__ = ["merge_markdown_files", "DEFAULT_DELIMITER", "DEFAULT_HEADING_LEVEL"]
