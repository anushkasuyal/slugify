# slugify

A small Python CLI for renaming files and directories into lowercase, hyphen-separated, ASCII-friendly names.

## Install

From the project directory, install it with:

```bash
pip install -e .
```

## Usage

```bash
slugify .
slugify Downloads
slugify . --recursive
slugify . --dry-run
slugify . --keep-case
slugify . --apply
```

By default, the tool previews changes without renaming anything. Use `--apply` to perform the renames.
