# vatrix/utils/pathing.py

import os
from pathlib import Path
from datetime import datetime
from appdirs import user_data_dir
import logging

logger = logging.getLogger(__name__)

APP_NAME = "vatrix"

def ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def get_input_path(filename: str, subdir: str = "inputs") -> Path:
    """
    Resolve the full path to an input file.
    Priority:
      1. CWD/inputs/
      2. user/appdata/inputs/ (if CWD not found)
    """
    cwd_path = Path.cwd() / subdir / filename
    if cwd_path.exists():
        logger.debug(f"📂 Resolved input path: {cwd_path}")
        return cwd_path

    fallback_path = Path(user_data_dir(APP_NAME)) / subdir / filename
    if fallback_path.exists():
        logger.debug(f"📂 Resolved input path: {fallback_path}")
        return fallback_path
    
    logger.warning(f"⚠️ Input file not found: {filename}")
    return fallback_path


def get_output_path(
    filename: str,
    use_cwd: bool = False,
    subdir: str = "outputs",
    timestamp: bool = False,
    ext: str = None
) -> Path:
    """
    Resolves a safe output path for generated files.

    :param filename: Base filename (e.g., 'logs.csv')
    :param use_cwd: If True, use current working directory. Otherwise use OS data dir.
    :param subdir: Optional subdirectory to organize outputs.
    :param timestamp: If True, inject a timestamp into the filename.
    :param ext: Optional extension override (e.g. 'json')
    :return: A resolved and writable Path
    """
    base = Path.cwd() if use_cwd else Path(user_data_dir(APP_NAME))
    
    if timestamp:
        name, suffix = os.path.splitext(filename)
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp_str}{ext or suffix}"

    full_path = base / subdir / filename
    logger.debug(f"🧭 Resolved path: {full_path}")
    return ensure_dir(full_path)
