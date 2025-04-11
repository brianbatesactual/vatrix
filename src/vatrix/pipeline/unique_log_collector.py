# src/vatrix/pipeline/hasher.py

import hashlib
import json
import threading


class UniqueLogCollector:
    def __init__(self):
        self._seen_hashes = set()
        self._unique_logs = []
        self._lock = threading.Lock()

    def _hash_event(self, event: dict) -> str:
        # Create a stable hash from sorted JSON
        serialized = json.dumps(event, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def add_if_unique(self, event: dict) -> bool:
        """
        Adds the event if it's unique.
        Returns True if added, False if duplicate.
        """
        event_hash = self._hash_event(event)

        with self._lock:
            if event_hash in self._seen_hashes:
                return False
            self._seen_hashes.add(event_hash)
            self._unique_logs.append(event)
            return True

    def get_all(self):
        with self._lock:
            return list(self._unique_logs)

    def export_to_jsonl(self, filepath):
        with self._lock, open(filepath, "w") as f:
            for event in self._unique_logs:
                f.write(json.dumps(event) + "\n")
