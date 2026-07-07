import argparse
import re
import sys
import unicodedata
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="slugify", description="Slugify filenames and directories")
    parser.add_argument("path", nargs="?", default=".", help="Directory to process")
    parser.add_argument("--recursive", action="store_true", help="Process subfolders recursively")
    parser.add_argument("--apply", action="store_true", help="Actually rename files and directories")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying them")
    parser.add_argument("--keep-case", action="store_true", help="Preserve original casing")
    return parser


def split_name_and_extension(name: str) -> tuple[str, str]:
    path = Path(name)
    suffixes = path.suffixes
    if suffixes:
        extension = "".join(suffixes)
        stem = name[: -len(extension)]
        return stem, extension
    return name, ""


def slugify_name(name: str, keep_case: bool = False) -> str:
    stem, extension = split_name_and_extension(name)
    transliterated = unicodedata.normalize("NFKD", stem)
    ascii_text = transliterated.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.replace("&", " and ")
    ascii_text = ascii_text.replace("+", " plus ")
    ascii_text = ascii_text.replace("@", " at ")
    ascii_text = re.sub(r"[^0-9A-Za-z]+", "-", ascii_text)
    ascii_text = re.sub(r"-+", "-", ascii_text).strip("-")
    if not ascii_text:
        ascii_text = "item"
    if not keep_case:
        ascii_text = ascii_text.lower()
    if extension:
        extension = extension.lower() if not keep_case else extension
        return f"{ascii_text}{extension}"
    return ascii_text


def resolve_target_name(current_name: str, desired_name: str, existing_names: set[str]) -> str:
    if desired_name == current_name:
        return current_name
    if desired_name not in existing_names:
        return desired_name
    stem, extension = split_name_and_extension(desired_name)
    counter = 2
    while True:
        candidate = f"{stem}-{counter}{extension}" if extension else f"{stem}-{counter}"
        if candidate not in existing_names:
            return candidate
        counter += 1


def process_directory(path: Path, recursive: bool, apply: bool, keep_case: bool) -> None:
    if not path.exists() or not path.is_dir():
        return

    entries = sorted(path.iterdir(), key=lambda item: item.name)
    existing_names = {entry.name for entry in entries}
    planned_moves: list[tuple[Path, str]] = []

    for entry in entries:
        desired_name = slugify_name(entry.name, keep_case=keep_case)
        target_name = resolve_target_name(entry.name, desired_name, existing_names)
        if target_name != entry.name:
            planned_moves.append((entry, target_name))
        existing_names.remove(entry.name)
        existing_names.add(target_name)

    for entry, target_name in planned_moves:
        source = entry
        destination = path / target_name
        if target_name != entry.name:
            action = "Renamed" if apply else "Would rename"
            print(f"{action}: {entry.name} -> {target_name}")
            if apply:
                source.rename(destination)

    if recursive:
        for child in sorted(path.iterdir(), key=lambda item: item.name):
            if child.is_dir():
                process_directory(child, recursive=True, apply=apply, keep_case=keep_case)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:])
    target = Path(args.path).expanduser().resolve()
    if not target.exists() or not target.is_dir():
        parser.error(f"{target} is not a directory")
    apply = args.apply
    process_directory(target, recursive=args.recursive, apply=apply, keep_case=args.keep_case)
    return 0
