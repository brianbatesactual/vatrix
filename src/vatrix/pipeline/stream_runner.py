# vatrix/pipeline/stream_runner.py

import json
import logging

from vatrix.templates.tmanager import TManager
from vatrix.templates.loader import load_template_map
from vatrix.pipeline.context_builder import build_context
from vatrix.inputs.stream_reader import read_from_stdin
from vatrix.outputs.file_writer import write_to_json
from vatrix.outputs.rotating_writer import RotatingStreamWriter

logger = logging.getLogger(__name__)

stream_writer = RotatingStreamWriter()

def process_stream(unmatched_json=None, render_mode='random', write_output=True, writer=None):
    template_manager = TManager()
    template_map = load_template_map()
    writer = writer or stream_writer

    unmatched_logs = []
    rendered_count = 0

    for log_entry in read_from_stdin():
        logger.debug(f"📥 Received line: {json.dumps(log_entry)}")
        context = build_context(log_entry)

        template_name = template_map.get(log_entry.get('TXSUBCLSID'), 'default_template.txt')
        if template_name == 'default_template.txt':
            logger.warning(f"TXSUBCLSID '{log_entry.get('TXSUBCLSID')}' not found. Using default template.")
            unmatched_logs.append(log_entry)
        else:
            rendered = template_manager.render_random_template(template_name, context)
            if write_output:
               writer.write(rendered)
            rendered_count += 1
            logger.info(f"✅ Rendered log with template: {template_name}")

    logger.info(f"📝 Stream ended. {rendered_count} logs {'written to disk' if write_output else 'processed in memory'}.")

    if unmatched_logs and write_output:
        write_to_json(file_path=unmatched_json, data=unmatched_logs)
        logger.warning(f"⚠️ {len(unmatched_logs)} unmatched logs saved.")