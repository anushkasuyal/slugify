from pathlib import Path

import pytest

from slugify.cli import build_parser, main


@pytest.fixture
def temp_dir(tmp_path):
    target = tmp_path / "sample"
    target.mkdir()
    (target / "Résumé (Final) & Notes.PDF").write_text("pdf")
    (target / "space name.txt").write_text("txt")
    return target


def test_parser_defaults_to_dry_run(capsys, temp_dir):
    parser = build_parser()
    args = parser.parse_args([str(temp_dir)])
    assert args.path == str(temp_dir)
    assert not args.apply
    assert args.dry_run is False


def test_main_dry_run_outputs_preview(tmp_path, capsys):
    target = tmp_path / "demo"
    target.mkdir()
    (target / "Résumé (Final) & Notes.PDF").write_text("x")

    import sys

    sys.argv = ["slugify", str(target)]
    exit_code = main()

    out = capsys.readouterr().out
    assert exit_code == 0
    assert "resume-final-and-notes.pdf" in out
    assert (target / "Résumé (Final) & Notes.PDF").exists()


def test_apply_renames_files(tmp_path):
    target = tmp_path / "demo"
    target.mkdir()
    (target / "Résumé (Final) & Notes.PDF").write_text("x")

    import sys

    sys.argv = ["slugify", str(target), "--apply"]
    exit_code = main()

    assert exit_code == 0
    assert not (target / "Résumé (Final) & Notes.PDF").exists()
    assert (target / "resume-final-and-notes.pdf").exists()


def test_recursive_apply_visits_subdirectories(tmp_path):
    target = tmp_path / "demo"
    subdir = target / "My Folder"
    subdir.mkdir(parents=True)
    (subdir / "Résumé.txt").write_text("x")

    import sys

    sys.argv = ["slugify", str(target), "--recursive", "--apply"]
    exit_code = main()

    assert exit_code == 0
    assert (target / "my-folder").exists()
    assert (target / "my-folder" / "resume.txt").exists()


def test_apply_reports_permission_errors_and_continues(tmp_path, capsys, monkeypatch):
    target = tmp_path / "demo"
    target.mkdir()
    (target / "Résumé.txt").write_text("x")
    (target / "space name.txt").write_text("y")

    original_rename = Path.rename

    def failing_rename(self, target_path):
        if self.name == "Résumé.txt":
            raise PermissionError("Access denied")
        return original_rename(self, target_path)

    monkeypatch.setattr(Path, "rename", failing_rename)

    import sys

    sys.argv = ["slugify", str(target), "--apply"]
    exit_code = main()

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "PermissionError" in captured.err
    assert (target / "Résumé.txt").exists()
    assert (target / "space-name.txt").exists()
