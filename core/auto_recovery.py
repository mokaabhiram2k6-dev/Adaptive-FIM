
import json
from pathlib import Path

from core.hashing import calculate_hash
from protection.recovery import restore_backup


PROTECTED_FOLDER = Path("protected_files")
MANIFEST_FILE = Path("snapshot_manifest.json")


def recover_modified_file(filename):

    if Path(filename).name != filename:
        raise ValueError("Invalid filename")

    if not MANIFEST_FILE.exists():
        raise FileNotFoundError("Snapshot manifest not found")

    with MANIFEST_FILE.open("r", encoding="utf-8") as file:
        manifest = json.load(file)

    if filename not in manifest:
        raise ValueError("No trusted snapshot available")

    snapshot = manifest[filename]

    backup_path = Path(snapshot["backup_file"])
    expected_hash = snapshot["original_hash"]
    target_path = PROTECTED_FOLDER / filename

    if not backup_path.is_file() or backup_path.is_symlink():
        raise ValueError("Trusted backup is missing or invalid")

    backup_hash = calculate_hash(backup_path)

    if backup_hash != expected_hash:
        raise ValueError("Backup integrity verification failed")

    if target_path.is_symlink():
        raise ValueError("Symbolic link restoration is not allowed")

    confirmation = input(
        f"Restore original version of {filename}? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        return {"status": "RECOVERY CANCELLED"}

    result = restore_backup(
        backup_path,
        target_path,
        expected_hash
    )

    return result


if __name__ == "__main__":

    filename = input("Enter filename to recover: ").strip()

    try:
        result = recover_modified_file(filename)
        print("\nRECOVERY RESULT")
        print(result)

    except Exception as error:
        print("\nRECOVERY FAILED:", error)
