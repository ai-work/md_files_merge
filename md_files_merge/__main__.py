"""Command line interface for the Markdown merger."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .merger import DEFAULT_DELIMITER, DEFAULT_HEADING_LEVEL, merge_markdown_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Merge Markdown files from a directory tree into a single Markdown "
            "document."
        )
    )
    parser.add_argument(
        "root",
        type=Path,
        help="Directory to search recursively for Markdown files.",
    )
    parser.add_argument(
        "output",
        type=Path,
        help="File path where the merged Markdown document will be written.",
    )
    parser.add_argument(
        "--heading-level",
        type=int,
        default=DEFAULT_HEADING_LEVEL,
        help=(
            "Heading level (1-6) used to separate individual Markdown files in "
            "the merged output."
        ),
    )
    parser.add_argument(
        "--delimiter",
        default=DEFAULT_DELIMITER,
        help=(
            "Delimiter that wraps each heading to keep it distinct from "
            "existing content."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> Path:
    parser = build_parser()
    args = parser.parse_args(argv)
    output_path = merge_markdown_files(
        args.root,
        args.output,
        heading_level=args.heading_level,
        delimiter=args.delimiter,
    )
    print(f"Merged Markdown written to {output_path}")
    return output_path


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
