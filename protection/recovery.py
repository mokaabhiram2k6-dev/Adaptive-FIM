
import shutil
import hashlib
from pathlib import Path


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def restore_backup(backup_path, target_path, expected_hash):
    """
    Restore a backup only after verifying its hash.
    """

    backup = Path(backup_path)
    target = Path(target_path)

    if not backup.is_file() or backup.is_symlink():
        raise ValueError("Invalid backup file")

    if target.is_symlink():
        raise ValueError("Symbolic links cannot be restored")

    backup_hash = calculate_hash(backup)

    if backup_hash != expected_hash:
        raise ValueError("Backup verification failed")

    target.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy2(backup, target)

    restored_hash = calculate_hash(target)

    if restored_hash != expected_hash:
        raise IOError("Restoration verification failed")

    return {
        "restored_file": str(target),
        "sha256": restored_hash,
        "status": "RECOVERY SUCCESSFUL"
    }
