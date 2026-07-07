# slugify

A small Python CLI for renaming files and directories into lowercase, hyphen-separated, ASCII-friendly names.

I usually use this as a pre-processing step before copying over files/folders from Windows to WSL!

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


<img width="161" height="116" alt="image" src="https://github.com/user-attachments/assets/7a1755c8-fa5a-42f8-9068-3184c4a25b96" />


```bash
>> slugify files --recursive --apply

Renamed: More files -> more-files
Renamed: My file.txt -> my-file.txt
Renamed: My files.txt -> my-files.txt
Renamed: (Some more) text files.txt -> some-more-text-files.txt
Renamed: Another directory (again) -> another-directory-again
Renamed: & One last file.docx -> and-one-last-file.docx
```


<img width="140" height="114" alt="image" src="https://github.com/user-attachments/assets/ba975f76-37be-4d29-87f0-f288f0d9a96a" />

