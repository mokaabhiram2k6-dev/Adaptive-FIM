
import hashlib
from pathlib import Path


def calculate_hash(file_path):
    """
    Generate a SHA-256 fingerprint for a file.
    Reads files in chunks to support large files.
    """

    sha256 = hashlib.sha256()

    file_path = Path(file_path)

    with file_path.open("rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def verify_integrity(file_path, trusted_hash):
    """
    Compare the current file hash with its trusted hash.
    """

    current_hash = calculate_hash(file_path)

    return current_hash == trusted_hash
