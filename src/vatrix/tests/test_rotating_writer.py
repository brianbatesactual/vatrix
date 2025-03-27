# tests/test_rotating_writer.py

from vatrix.outputs.rotating_writer import RotatingStreamWriter
import time
import random

def simulate_stream_write(total_lines=1000, simulate_size_mb=False):
    writer = RotatingStreamWriter(
        subdir="test_stream_output",
        max_days=.001,
        max_total_gb=0.001,   # ~1MB for fast test
        max_file_mb=0.1       # rotate every ~100KB
    )

    for i in range(total_lines):
        sentence = f"Test sentence #{i} - " + ("x" * (1024 if simulate_size_mb else 10))  # ~1KB or 10B payload
        writer.write(sentence)

        if i % 100 == 0:
            print(f"Wrote {i} lines...")
            time.sleep(0.1)

    print("✅ Stream simulation complete.")

if __name__ == "__main__":
    simulate_stream_write()

    '''
    pro tip: watch -n 1 'du -ch ~/.local/share/vatrix/test_stream_output/*.csv | tail -n 10'

    '''
