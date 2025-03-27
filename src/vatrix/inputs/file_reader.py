# vatrix/inputs/file_reader.py

import os
import json
import logging
import importlib.resources as pkg_resources

from pathlib import Path
from vatrix.utils.pathing import get_input_path

logger = logging.getLogger(__name__)

def read_from_default_data():
    logger.info("📁 No input file specified. Using built-in sample logs.")
    
    try:
        with pkg_resources.files("vatrix.sample_logs").joinpath("input_logs.ndjson").open("r") as f:
            logs = []
            for line in f:
                try:
                    logs.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    logger.warning("⚠️ Skipping invalid JSON line in sample logs.")
            logger.info(f"✅ Loaded {len(logs)} sample logs from bundled data.")
            return logs
    except FileNotFoundError:
        logger.error("🚫 Sample log file not found in package. Check packaging or install.")
        raise

def read_json_lines(file_path):
    file_path = str(file_path)

    if not os.path.exists(file_path):
        logger.error(f"🚫 File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    logs = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                logs.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                logger.warning("⚠️ Skipping invalid JSON line.")
                continue

    logger.info(f"✅ Loaded {len(logs)} logs from: {file_path}")
    return logs