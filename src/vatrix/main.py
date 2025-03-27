# src/main.py

import logging

from vatrix.cli.args import parse_args
from vatrix.utils.logger import setup_logger
from vatrix.inputs import file_reader
from vatrix.pipeline.processor import process_logs
from vatrix.pipeline.stream_runner import process_stream
from vatrix.utils.banner import get_banner

def main():
    print(get_banner())
    
    args = parse_args()

    # logging init
    log_path = setup_logger(
        level=getattr(logging, args.log_level.upper(), "INFO"),
        log_file=args.log_file,
        mode=args.mode
    )   

    args.log_file = log_path

    logger = logging.getLogger(__name__)
    
    logger.info("✅ Logging system initialized")
    logger.info("Starting vatrix pipeline...")
    logger.info(f"Mode: {args.mode} | Render mode: {args.render_mode} | SBERT Data: {args.generate_sbert_data}")

    # file mode
    if args.mode == 'file':
        logger.info(f"📁 File mode selected. Reading logs from {args.input}")
        
        if args.input:
            logger.info(f"📥 Reading logs from {args.input}")
            logs = file_reader.read_json_lines(args.input)
        else:
            logs = file_reader.read_from_default_data()
        
        logger.info(f"📊 Loaded {len(logs)} logs from input file.")
        process_logs(
            logs,
            output_csv=args.output,
            unmatched_json=args.unmatched,
            render_mode=args.render_mode,
            generate_sbert=args.generate_sbert_data
        )

    # stream mode
    elif args.mode == 'stream':
        logger.info(f"🌊 Stream mode selected. Waiting for NSJSON from standard input.")
        process_stream(
            unmatched_json=args.unmatched,
            render_mode=args.render_mode,
            write_output=False
        )
        
    else:
        if args.input_file:
            logs = file_reader.read_json_lines(args.input_file)
        else:
            logs = file_reader.read_from_default_data()
        process_stream(
            logs, 
            args.output, 
            args.unmatched, 
            render_mode=args.render_mode,
            write_output=True
        )

if __name__ == "__main__":
    main()