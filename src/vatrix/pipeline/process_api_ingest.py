import os
import logging
from vatrix.templates.tmanager import TManager
from vatrix.templates.loader import load_template_map
from vatrix.pipeline.context_builder import build_context
from vatrix.outputs.rotating_writer import RotatingStreamWriter
from vatrix.outputs.qdrant_writer import QdrantWriter
from vatrix.pipeline.embedding_pipeline import EmbeddingPipeline
from vatrix.pipeline.unique_log_collector import UniqueLogCollector

logger = logging.getLogger(__name__)

# Shared components
stream_writer = RotatingStreamWriter()
embedding_pipeline = EmbeddingPipeline()
qdrant_writer = QdrantWriter()
unique_collector = UniqueLogCollector()
template_manager = TManager()
template_map = load_template_map()

def process_api_ingest(log_entry: dict):
    logger.debug(f"📥 Ingesting log from API: {log_entry}")

    is_unique = unique_collector.add_if_unique(log_entry)
    if not is_unique:
        logger.debug("⏭️ Duplicate log skipped")
        return

    context = build_context(log_entry)
    template_name = template_map.get(log_entry.get('TXSUBCLSID'), 'default_template.txt')

    if template_name == 'default_template.txt':
        logger.warning(f"⚠️ No template match for TXSUBCLSID={log_entry.get('TXSUBCLSID')}")
        return

    rendered = template_manager.render_random_template(template_name, context)
    stream_writer.write(rendered)

    vector = embedding_pipeline.encode(rendered)
    metadata = {
        "timestamp": log_entry.get("timestamp"),
        "host": log_entry.get("host"),
        "source": log_entry.get("source"),
        "template": template_name
    }
    if os.getenv("VATRIX_DEBUG", "false") == "true":
        print(f"🔎 EMBEDDING: '{rendered}'\\n→ Vector: {vector[:5]}...")

    qdrant_writer.add_to_buffer(vector, metadata)

    logger.info(f"✅ Ingest complete: {template_name}")
