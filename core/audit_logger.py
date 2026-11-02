
import json
from pathlib import Path
from datetime import datetime


LOG_FILE = Path("security_audit.json")


def log_event(event_type, details):

    event = {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        "event_type": event_type,
        "details": details
    }

    if LOG_FILE.exists():
        with LOG_FILE.open("r", encoding="utf-8") as file:
            try:
                logs = json.load(file)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    logs.append(event)

    with LOG_FILE.open("w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)

    return event
