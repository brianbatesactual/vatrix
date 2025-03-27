# 	src/vatrix/pipeline/processor.py

import logging

from vatrix.templates.tmanager import TManager
from vatrix.templates.loader import load_template_map
from vatrix.pipeline.context_builder import build_context
from vatrix.outputs.file_writer import write_to_csv, write_to_json
from vatrix.outputs.sbert_writer import export_sentence_pairs
from vatrix.utils.similarity import get_similarity_score


logger = logging.getLogger(__name__)

def process_logs(logs, output_csv, unmatched_json, render_mode='random', generate_sbert=False):
    logger.info(f"🔧 Processing {len(logs)} log entries")
    template_manager = TManager()

    processed_logs = []
    unmatched_logs = []
    sbert_pairs = []

    template_map = load_template_map()
    logger.debug(f"🧭 Template map loaded: {list(template_map.keys())}")

    for log_entry in logs:
        context = build_context(log_entry)

        template_name = template_map.get(log_entry['TXSUBCLSID'], 'default_template.txt')
        
        if template_name == 'default_template.txt':
            logger.warning(f"TXSUBCLSID '{log_entry.get('TXSUBCLSID')}' not found. Using default template.")
            unmatched_logs.append(log_entry)
            logger.warning(f"⚠️ {len(unmatched_logs)} unmatched logs written to {unmatched_json}")

        else:
            if render_mode == 'random':
                rendered_text = template_manager.render_random_template(template_name, context)
                processed_logs.append({'log': rendered_text})
                logger.info(f"✅ Rendered {len(processed_logs)} logs")
            
            elif render_mode == 'all':
                rendered_texts = template_manager.render_all_templates(template_name, context)
                processed_logs.extend([{'log': t} for t in rendered_texts])
                logger.info(f"✅ Rendered {len(processed_logs)} logs")

                if generate_sbert:
                    base = rendered_texts[0]
                    for variation in rendered_texts[1:]:
                        sim_score = get_similarity_score(base, variation)
                        sbert_pairs.append((base, variation, sim_score)) # all variations are highly similar
                logger.info(f"📊 Generated {len(sbert_pairs)} SBERT training pairs")

            else:
                raise ValueError('Invalid render mode. Use "random" or "all".')

    if generate_sbert:
        export_sentence_pairs(sbert_pairs)
        logger.info(f'📦 Export complete for {len(sbert_pairs)} SBERT training pairs.')

    if processed_logs:
        write_to_csv(file_path=output_csv, rows=processed_logs, fieldnames=['log'])

    if unmatched_logs:
        write_to_json(file_path=unmatched_json, data=unmatched_logs)