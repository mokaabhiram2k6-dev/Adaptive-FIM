
import json
from pathlib import Path

from core.monitoring import check_integrity
from core.risk_engine import calculate_risk
from core.audit_logger import log_event
from core.auto_recovery import recover_modified_file


ROOT = Path(__file__).resolve().parent
PROTECTED_FOLDER = ROOT / "protected_files"
BASELINE_FILE = ROOT / "baseline.json"


def safe_log(event_type, details):
    """Record security events without interrupting monitoring."""
    try:
        log_event(event_type, details)
    except Exception as error:
        print("AUDIT LOG ERROR:", error)


def run_adaptive_fim():

    print("\n========== ADAPTIVE FIM ==========")
    print("Starting File Integrity Monitoring...\n")

    # STEP 1: Load baseline
    if not BASELINE_FILE.exists():
        print("ERROR: Baseline file not found!")
        return

    try:
        with BASELINE_FILE.open("r", encoding="utf-8") as file:
            baseline = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print("BASELINE ERROR:", error)
        return

    # STEP 2: Monitor protected files
    results = check_integrity(
        str(PROTECTED_FOLDER),
        baseline
    )

    modified = results.get("modified", [])
    deleted = results.get("deleted", [])
    new_files = results.get("new_files", [])
    errors = results.get("errors", [])

    print("========== FILE MONITORING ==========")

    print("Modified Files:", modified)
    print("Deleted Files:", deleted)
    print("New Files:", new_files)
    print("Errors:", errors)

    # STEP 3: Calculate risk
    changes = (
        len(modified)
        + len(deleted)
        + len(new_files)
    )

    risk = calculate_risk(
        min(changes * 30, 100),
        5,
        changes > 0
    )

    print("\n========== RISK ASSESSMENT ==========")

    print("Risk Score:", risk["risk_score"])
    print("Risk Level:", risk["risk_level"])

    safe_log("SCAN_COMPLETED", {
        "modified_files": modified,
        "deleted_files": deleted,
        "new_files": new_files,
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "monitoring_errors": errors
    })

    # STEP 4: Recovery
    print("\n========== AUTOMATIC RECOVERY ==========")

    recovery_files = modified + deleted

    if not recovery_files:
        print("No modified or deleted files detected.")

    for filename in recovery_files:

        print("\nSuspicious File:", filename)

        try:
            recovery_result = recover_modified_file(filename)

            print("Recovery Result:", recovery_result)

            safe_log("RECOVERY_ATTEMPT", {
                "filename": filename,
                "result": recovery_result
            })

        except Exception as error:

            print("RECOVERY FAILED:", error)

            safe_log("RECOVERY_FAILED", {
                "filename": filename,
                "reason": str(error)
            })

    # STEP 5: New file detection
    print("\n========== NEW FILE ANALYSIS ==========")

    if new_files:
        for filename in new_files:

            print("Unrecognized File:", filename)
            print("Action: Manual inspection required.")

            safe_log("NEW_FILE_DETECTED", {
                "filename": filename,
                "action": "Manual inspection required"
            })
    else:
        print("No new files detected.")

    # STEP 6: Final security report
    print("\n========== FINAL SECURITY REPORT ==========")

    print("Total Changes:", changes)
    print("Modified Files:", len(modified))
    print("Deleted Files:", len(deleted))
    print("New Files:", len(new_files))
    print("Risk Score:", risk["risk_score"])
    print("Risk Level:", risk["risk_level"])
    print("Monitoring Errors:", len(errors))

    print("\nAudit Log:", ROOT / "security_audit.json")

    print("\n========== SCAN COMPLETE ==========")


if __name__ == "__main__":
    run_adaptive_fim()
