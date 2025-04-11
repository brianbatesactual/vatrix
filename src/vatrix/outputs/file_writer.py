# src/vatrix/outputs/file_writer.py

import atexit
import csv
import json
import os
import threading
from datetime import datetime

from vatrix.utils.pathing import get_output_path

BUFFER = []
BUFFER_LOCK = threading.Lock()
BUFFER_LIMIT = 20
PROCESS_CALLBACK = None

ROTATE_PATH = "stream_output/"
os.makedirs(ROTATE_PATH, exist_ok=True)


def write_to_buffered_csv(event: dict, metadata: dict):
    global BUFFER
    row = {
        "timestamp": metadata.get("time", datetime.utcnow().isoformat()),
        "host": metadata.get("host", "unknown"),
        **event,
    }

    if PROCESS_CALLBACK:
        PROCESS_CALLBACK(row)

    with BUFFER_LOCK:
        BUFFER.append(row)
        if len(BUFFER) >= BUFFER_LIMIT:
            flush_buffer_to_file()


def flush_buffer_to_file():
    global BUFFER
    if not BUFFER:
        return

    now = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"{ROTATE_PATH}/splunk_events_{now}.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=BUFFER[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(BUFFER)
    BUFFER = []


def read_json_file(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            log_entry = json.loads(line.strip())
            data.append(log_entry)
        return data


def write_to_csv(file_path=None, rows=None, fieldnames=None):
    if file_path is None:
        file_path = get_output_path("processed_logs.csv", timestamp=True, subdir="outputs")

    with open(file_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerows(rows)


def write_to_json(file_path=None, data=None):
    if file_path is None:
        file_path = get_output_path("unmatched.json", timestamp=True, subdir="unmatched")

    with open(file_path, "a", newline="") as file:
        json.dump(data, file, indent=4)


# Register shutdown hook to flush buffer
atexit.register(flush_buffer_to_file)
