import json
import os
from datetime import datetime, timezone

log_path = os.path.join(
    os.path.dirname(__file__),
    "../../results/audit_log.jsonl"
)

os.makedirs(os.path.dirname(log_path), exist_ok=True)

def save_audit_log(entry: dict):
    entry["timestamp"] = datetime.now(timezone.utc).isoformat()

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")