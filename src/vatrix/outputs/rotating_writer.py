# vatrix/outputs/rotating_writer.py

import os
import csv
import time
from pathlib import Path
from datetime import datetime, timedelta
import logging

from vatrix.utils.pathing import get_output_path

logger = logging.getLogger(__name__)

class RotatingStreamWriter:
    def __init__(self, subdir="stream_output", max_days=7, max_total_gb=20, max_file_mb=1024):
        self.subdir = subdir
        self.max_days = max_days
        self.max_total_gb = max_total_gb
        self.max_file_mb = max_file_mb
        self.current_path = None
        self.current_file = None
        self.csv_writer = None
        self.fieldnames = ['log']
        self.last_rotation = None

    def _rotate_if_needed(self):
        now = datetime.now()
        should_rotate = False

        if not self.current_path:
            should_rotate = True
        elif (now - self.last_rotation) > timedelta(hours=24):
            should_rotate = True
        elif os.path.getsize(self.current_path) > self.max_file_mb * 1024 * 1024:
            should_rotate = True

        if should_rotate:
            if self.current_file:
                self.current_file.close()

            self.current_path = get_output_path(
                filename="streamed_logs.csv",
                timestamp=True,
                subdir=self.subdir,
                use_cwd=False
            )

            self.current_file = open(self.current_path, 'w', newline='', encoding='utf-8')
            self.csv_writer = csv.DictWriter(self.current_file, fieldnames=self.fieldnames)
            self.csv_writer.writeheader()
            self.last_rotation = now

            logger.info(f"🔄 Started new stream file: {self.current_path}")

            self._enforce_retention()

    def _enforce_retention(self):
        dir_path = self.current_path.parent
        all_files = list(dir_path.glob("*.csv"))
        all_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        total_size = 0
        now = time.time()

        for f in all_files:
            age_days = (now - f.stat().st_mtime) / (60 * 60 * 24)
            size_bytes = f.stat().st_size
            total_size += size_bytes

            if age_days > self.max_days or (total_size / 1e9) > self.max_total_gb:
                logger.info(f"🧹 Deleting old stream file: {f.name}")
                try:
                    f.unlink()
                except Exception as e:
                    logger.warning(f"Failed to delete {f.name}: {e}")

    def write(self, sentence):
        self._rotate_if_needed()
        self.csv_writer.writerow({'log': sentence})
        self.current_file.flush()
