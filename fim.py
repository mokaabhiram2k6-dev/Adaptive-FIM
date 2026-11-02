import os
import hashlib
import json

FOLDER = "protected_files"
BASELINE_FILE = "baseline.json"


def calculate_hash(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


# Load trusted baseline
with open(BASELINE_FILE, "r") as file:
    baseline = json.load(file)

print("========== FILE INTEGRITY MONITOR ==========")
print("Checking protected files...\n")


# Get all files currently present
current_files = set(
    filename for filename in os.listdir(FOLDER)
    if os.path.isfile(os.path.join(FOLDER, filename))
)


# Check original files
for filename, old_hash in baseline.items():

    filepath = os.path.join(FOLDER, filename)

    # Deleted file
    if not os.path.exists(filepath):
        print(f"🗑️ ALERT: {filename} has been DELETED!")
        continue

    # Current hash
    current_hash = calculate_hash(filepath)

    # Modified file
    if current_hash != old_hash:
        print(f"🚨 {filename} : FILE MODIFIED!")
        print(f"   Previous Hash : {old_hash}")
        print(f"   Current Hash  : {current_hash}")
        print("   Status        : INTEGRITY VIOLATION\n")

    else:
        print(f"✅ {filename} : No Change")


# Check for new files
for filename in current_files:

    if filename not in baseline:
        print(f"\n⚠️ NEW FILE DETECTED: {filename}")
        print("   Status : UNAUTHORIZED FILE")