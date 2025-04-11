# src/vatrix/outputs/sbert_writer.py

import csv
import logging
from datetime import datetime

from vatrix.utils.pathing import get_output_path

logger = logging.getLogger(__name__)


def export_sentence_pairs(pairs, file_path=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if file_path is None:
        file_path = get_output_path("sentence_pairs.csv", timestamp=True, subdir="training")

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sentence1", "sentence2", "score"])
        for s1, s2, score in pairs:
            writer.writerow([s1, s2, score])

    logger.info(f"📦 Exported {len(pairs)} SBERT training pairs to {file_path}")
