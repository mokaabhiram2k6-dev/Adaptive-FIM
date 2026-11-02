
import json
from pathlib import Path

from core.hashing import calculate_hash
from protection.backup import create_backup


PROTECTED_FOLDER = Path("protected_files")
BASELINE_FILE = Path("baseline.json")
MANIFEST_FILE = Path("snapshot_manifest.json")


def create_trusted_snapshots():

    if not BASELINE_FILE.exists():
        raise FileNotFoundError("Baseline file not found")

    with BASELINE_FILE.open("r", encoding="utf-8") as file:
        baseline = json.load(file)

    manifest = {}
    results = {
        "backed_up": [],
        "modified": [],
        "missing": [],
        "errors": []
    }

    for filename, expected_hash in baseline.items():

        if Path(filename).name != filename:
            results["errors"].append(filename)
            continue

        file_path = PROTECTED_FOLDER / filename

        try:
            if not file_path.is_file() or file_path.is_symlink():
                results["missing"].append(filename)
                continue

            current_hash = calculate_hash(file_path)

            if current_hash != expected_hash:
                results["modified"].append(filename)
                continue

            backup_info = create_backup(file_path)

            manifest[filename] = {
                "original_hash": expected_hash,
                "backup_file": backup_info["backup_file"],
                "status": backup_info["status"]
            }

            results["backed_up"].append(filename)

        except Exception as error:
            results["errors"].append({
                "file": filename,
                "reason": str(error)
            })

    with MANIFEST_FILE.open("w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=4)

    return results


if __name__ == "__main__":

    print("TRUSTED SNAPSHOT MANAGEMENT")
    print("---------------------------")

    result = create_trusted_snapshots()

    for category, files in result.items():
        print(f"{category.upper()}: {files}")
