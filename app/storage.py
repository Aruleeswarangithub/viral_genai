import json
import os
from typing import List, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")


def ensure_storage():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)


def load_history() -> List[dict]:
    ensure_storage()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(records: List[dict]):
    ensure_storage()
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def add_record(record: dict):
    records = load_history()
    records.insert(0, record)
    save_history(records)


def get_record(job_id: str) -> Optional[dict]:
    records = load_history()
    for record in records:
        if record["job_id"] == job_id:
            return record
    return None


def update_record(job_id: str, updates: dict) -> Optional[dict]:
    records = load_history()
    updated_record = None
    for i, record in enumerate(records):
        if record["job_id"] == job_id:
            record.update(updates)
            records[i] = record
            updated_record = record
            break
    save_history(records)
    return updated_record
