# md_files_merge

Command line tool and Python utility for merging Markdown files from a
directory tree into a single document. The merger walks the target directory in
alphabetical order and prepends the contents of each Markdown file with a
synthetic heading that contains the file's relative path wrapped by a unique
delimiter (default: `<<<>>>`).

## Command line usage

Run the tool by executing the module directly:

```bash
python -m md_files_merge <root_directory> <output_file> [--heading-level N] [--delimiter TEXT]
```

**Arguments**

- `root_directory`: Directory to search recursively for `.md` files.
- `output_file`: Path to the Markdown file that will contain the merged
  contents.
- `--heading-level`: Optional heading level (1–6) for the synthetic headings.
- `--delimiter`: Optional delimiter to wrap the heading content and keep it
  unique from the original file contents.

## Programmatic usage

The merger can be imported and used from another Python module:

```python
from md_files_merge import merge_markdown_files

merge_markdown_files(
    "docs",
    "merged.md",
    heading_level=2,
    delimiter="<<<>>>",
)
```

The function returns the path to the generated Markdown file.
