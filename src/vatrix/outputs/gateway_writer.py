# outputs/gateway_writer.py
import logging
import os
from datetime import datetime
from typing import Dict, List

import requests

from vatrix.config.settings import (
    DEBUG_MODE,
    GATEWAY_INGEST_URL,
    GATEWAY_VERIFY_TLS,
    VATRIX_API_TOKEN,
)

AUTH_HEADER = {"Authorization": f"Bearer {VATRIX_API_TOKEN}"}


def send_to_gateway(project: str, embeddings: List[Dict]):

    # Send a batch of logs and embeddings to the Vatrix Gateway over REST.

    # embeddings: List of dicts with keys:
    #     - id: str
    #     - vector: List[float]
    #     - payload: dict

    payload = {
        "project": project,
        "entries": [
            {
                "id": e["id"],
                "vector": e["vector"],
                "payload": e["payload"],
                "timestamp": e["payload"].get("timestamp", datetime.utcnow().isoformat()),
            }
            for e in embeddings
        ],
    }

    try:
        import json

        logging.debug("📦 Sending payload:\n%s", json.dumps(payload, indent=2, default=str))
        response = requests.post(
            GATEWAY_INGEST_URL,
            headers=AUTH_HEADER,
            json=payload,
            verify=GATEWAY_VERIFY_TLS,
        )
        response.raise_for_status()
        logging.info(f"✅ Successfully shipped {len(embeddings)} vectors to Vatrix-Gateway.")
    except Exception as e:
        logging.error(f"❌ Failed to send data to Vatrix-Gateway: {e}")
