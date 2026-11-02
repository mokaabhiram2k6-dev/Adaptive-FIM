
import shutil
import hashlib
from pathlib import Path
from datetime import datetime


BACKUP_FOLDER = Path("backups")


def calculate_backup_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def create_backup(file_path):
    """
    Create and verify a timestamped backup.
    """

    source = Path(file_path)

    if not source.is_file() or source.is_symlink():
        raise ValueError("Invalid source file")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    destination_folder = BACKUP_FOLDER / source.name
    destination_folder.mkdir(parents=True, exist_ok=True)

    backup_path = destination_folder / f"{timestamp}_{source.name}"

    shutil.copy2(source, backup_path)

    original_hash = calculate_backup_hash(source)
    backup_hash = calculate_backup_hash(backup_path)

    if original_hash != backup_hash:
        backup_path.unlink()
        raise IOError("Backup verification failed")

    return {
        "original_file": str(source),
        "backup_file": str(backup_path),
        "sha256": backup_hash,
        "status": "BACKUP SUCCESSFUL"
    }
