import logging
import os
from datetime import datetime
from uuid import uuid4

from vatrix.outputs.gateway_writer import send_to_gateway
from vatrix.outputs.rotating_writer import RotatingStreamWriter
from vatrix.pipeline.context_builder import build_context
from vatrix.pipeline.embedding_pipeline import EmbeddingPipeline
from vatrix.pipeline.unique_log_collector import UniqueLogCollector
from vatrix.templates.loader import load_template_map
from vatrix.templates.tmanager import TManager

logger = logging.getLogger(__name__)

# Shared components
stream_writer = RotatingStreamWriter()
embedding_pipeline = EmbeddingPipeline()
unique_collector = UniqueLogCollector()
template_manager = TManager()
template_map = load_template_map()


def parse_timestamp(ts):
    try:
        if isinstance(ts, int):
            ts = str(ts)
        if len(ts) == 14:
            return datetime.strptime(ts, "%Y%m%d%H%M%S")
        elif isinstance(ts, str):
            return datetime.fromisoformat(ts)
        else:
            raise ValueError("Unrecognized timestamp format")
    except Exception as e:
        logger.warning(f"⚠️ Failed to parse timestamp: {ts} ({e}) — using current time.")
        return datetime.utcnow()


def process_api_ingest(log_entry: dict):
    logger.debug(f"📥 Ingesting log from API: {log_entry}")

    is_unique = unique_collector.add_if_unique(log_entry)
    if not is_unique:
        logger.debug("⏭️ Duplicate log skipped")
        return

    context = build_context(log_entry)
    template_name = template_map.get(log_entry.get("TXSUBCLSID"), "default_template.txt")

    if template_name == "default_template.txt":
        logger.warning(f"⚠️ No template match for TXSUBCLSID={log_entry.get('TXSUBCLSID')}")
        return

    rendered = template_manager.render_random_template(template_name, context)
    stream_writer.write(rendered)

    vector = embedding_pipeline.encode(rendered)
    parsed_ts = parse_timestamp(log_entry.get("CURRENT_TIMESTAMP"))

    # Parse timestamp format
    # timestamp_raw = log_entry.get("timestamp")  # e.g., 20250320015236
    # if isinstance(timestamp_raw, int):  # SAP style numeric
    #     timestamp_str = str(timestamp_raw)
    #     parsed_ts = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
    # else:
    #     parsed_ts = datetime.fromisoformat(timestamp_raw)

    # metadata = {
    #     "timestamp": parsed_ts.isoformat(),
    #     "host": log_entry.get("host"),
    #     "source": log_entry.get("source"),
    #     "template": template_name,
    # }

    payload_metadata = {k: str(v) for k, v in log_entry.items() if v is not None}
    payload_metadata["rendered"] = rendered
    payload_metadata["template"] = template_name

    entry = {
        "id": str(uuid4()),
        "vector": vector.tolist(),
        "payload": payload_metadata,
        "timestamp": parsed_ts,  # This must be a datetime object for Pydantic
    }

    if os.getenv("VATRIX_DEBUG", "false") == "true":
        print(f"🔎 EMBEDDING: '{rendered}'\\n→ Vector: {vector[:5]}...")

    # send_to_gateway.add_to_buffer(vector, metadata)
    send_to_gateway(project="vatrix-stream", embeddings=[entry])

    logger.info(f"✅ Ingest complete: {template_name}")
