# /src/vatrix/tests/test_gateway_integration.py
# v2 testing program

from datetime import datetime
from uuid import uuid4

import requests

from vatrix.config.settings import GATEWAY_INGEST_URL, GATEWAY_VERIFY_TLS, VATRIX_API_TOKEN
from vatrix.pipeline.embedding_pipeline import EmbeddingPipeline


def test_live_gateway_upsert():
    embedding = EmbeddingPipeline()
    sentence = "User DDIC logged in successfully to system X using method B"
    vector = embedding.encode(sentence).tolist()

    payload = {
        "project": "vatrix-test",
        "entries": [
            {
                "id": str(uuid4()),
                "vector": vector,
                "payload": {"rendered": sentence, "template": "test_logon"},
                "timestamp": datetime.utcnow().isoformat(),
            }
        ],
    }

    AUTH_HEADER = {"Authorization": f"Bearer {VATRIX_API_TOKEN}"}

    res = requests.post(
        GATEWAY_INGEST_URL, headers=AUTH_HEADER, json=payload, verify=GATEWAY_VERIFY_TLS
    )

    assert res.status_code == 200
    print("✅ Ingested test vector to gateway successfully")
