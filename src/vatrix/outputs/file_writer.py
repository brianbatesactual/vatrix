# src/vatrix/outputs/file_writer.py

import os
import csv
import json

from vatrix.utils.pathing import get_output_path

def read_json_file(file_path):
    data =[]
    with open(file_path, 'r') as file:
        for line in file:
            log_entry = json.loads(line.strip())
            data.append(log_entry)
        return data

def write_to_csv(file_path=None, rows=None, fieldnames=None):
    if file_path is None:
        file_path = get_output_path("processed_logs.csv", timestamp=True, subdir="outputs")
    
    # file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerows(rows)

def write_to_json(file_path=None, data=None):
    if file_path is None:
        file_path = get_output_path("unmatched.json", timestamp=True, subdir="unmatched")
    
    with open(file_path, 'a', newline='') as file:
        json.dump(data, file, indent=4)