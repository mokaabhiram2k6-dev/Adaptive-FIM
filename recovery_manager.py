
from pathlib import Path
from protection.recovery import restore_backup
from protection.backup import calculate_backup_hash


BACKUP_FOLDER = Path("backups")


def recover_file(filename):

    backup_directory = BACKUP_FOLDER / filename

    if not backup_directory.exists():
        print("No backup directory found.")
        return

    backup_files = sorted(
        [
            file for file in backup_directory.iterdir()
            if file.is_file() and not file.is_symlink()
        ],
        reverse=True
    )

    if not backup_files:
        print("No valid backups available.")
        return

    print("\nAvailable backups:")

    for index, backup in enumerate(backup_files, start=1):
        print(f"{index}. {backup.name}")

    try:
        choice = int(input("\nSelect backup number: "))

        if choice < 1 or choice > len(backup_files):
            print("Invalid selection.")
            return

        selected_backup = backup_files[choice - 1]

        expected_hash = calculate_backup_hash(selected_backup)

        target_path = Path("protected_files") / filename

        result = restore_backup(
            selected_backup,
            target_path,
            expected_hash
        )

        print("\n", result)

    except ValueError as error:
        print("Error:", error)

    except Exception as error:
        print("Recovery failed:", error)


if __name__ == "__main__":

    filename = input("Enter filename to recover: ").strip()

    if Path(filename).name != filename or filename in (".", ".."):
        print("Invalid filename.")
    else:
        recover_file(filename)
