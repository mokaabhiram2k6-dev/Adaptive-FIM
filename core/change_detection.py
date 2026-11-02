
import difflib
from pathlib import Path


def compare_file_content(old_content, new_content):
    """
    Compare previous and current file content.
    Returns the exact lines added and removed.
    """

    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()

    differences = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="Previous Version",
            tofile="Current Version",
            lineterm=""
        )
    )

    added_lines = []
    removed_lines = []

    for line in differences:
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])

        elif line.startswith("-") and not line.startswith("---"):
            removed_lines.append(line[1:])

    return {
        "added": added_lines,
        "removed": removed_lines,
        "diff": differences
    }


def compare_files(old_file, new_file):
    """
    Compare two text files and return their differences.
    """

    old_content = Path(old_file).read_text(
        encoding="utf-8",
        errors="replace"
    )

    new_content = Path(new_file).read_text(
        encoding="utf-8",
        errors="replace"
    )

    return compare_file_content(old_content, new_content)
