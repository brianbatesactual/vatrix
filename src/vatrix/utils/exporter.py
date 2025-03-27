

#deprecated

import csv
import os
import logging
from vatrix.utils.helpers import path_from_root

logger = logging.getLogger(__name__)

def export_sentence_pairs(pairs, file_path=None):
    if file_path is None:
        file_path = path_from_root('data/training/sentence_pairs.csv')

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['sentence1', 'sentence2', 'score'])
        for sent1, sent2, score in pairs:
            writer.writerow([sent1, sent2, score])

    logger.info(f"📦 Exported {len(pairs)} SBERT training pairs to {file_path}")
