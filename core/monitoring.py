
import os
from pathlib import Path

from core.hashing import calculate_hash


def scan_directory(folder_path):
    """
    Recursively scan a folder and calculate
    SHA-256 hashes for all files.
    """

    folder = Path(folder_path)
    file_hashes = {}
    errors = []

    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Invalid directory: {folder}")

    for root, dirs, files in os.walk(folder):

        # Avoid following symbolic-link directories
        dirs[:] = [
            name for name in dirs
            if not (Path(root) / name).is_symlink()
        ]

        for filename in files:
            file_path = Path(root) / filename

            if file_path.is_symlink():
                continue

            relative_path = file_path.relative_to(folder).as_posix()

            try:
                file_hashes[relative_path] = calculate_hash(file_path)

            except OSError as error:
                errors.append({
                    "file": relative_path,
                    "error": str(error)
                })

    return file_hashes, errors


def check_integrity(folder_path, baseline):
    """
    Compare all currently scanned files
    against the trusted baseline.
    """

    current_files, errors = scan_directory(folder_path)

    unchanged = []
    modified = []
    deleted = []
    new_files = []

    # Check existing trusted files
    for filename, old_hash in baseline.items():

        if filename not in current_files:
            deleted.append(filename)

        elif current_files[filename] != old_hash:
            modified.append(filename)

        else:
            unchanged.append(filename)

    # Detect files not present in baseline
    for filename in current_files:

        if filename not in baseline:
            new_files.append(filename)

    return {
        "unchanged": unchanged,
        "modified": modified,
        "deleted": deleted,
        "new_files": new_files,
        "errors": errors
    }
