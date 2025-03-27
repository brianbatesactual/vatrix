# tests/test_pipeline_end_to_end.py

import json
from io import StringIO
from unittest.mock import patch
from vatrix.pipeline.stream_runner import process_stream
from vatrix.outputs.rotating_writer import RotatingStreamWriter
from vatrix.utils.pathing import get_output_path
import os

def test_end_to_end_stream():
    print("🚀 End-to-end stream test...")
    # Simulated sample input
    test_logs = [
        {
            "TXSUBCLSID": "Dialog Logon",  # must exist in your template map!
            "ALGDATE": "2025-03-27",
            "ALGTIME": "14:55:12",
            "ALGUSER": "admin",
            "ALGCLIENT": "web",
            "ALGTEXT": "Login failed",
            "PARAM1": "192.168.0.1",
            "PARAM2": "admin",
            "ALGSYSTEM": "auth"
        },
        {
            "TXSUBCLSID": "UNKNOWN_TX",
            "ALGDATE": "2025-03-27",
            "ALGTIME": "15:00:00",
            "ALGUSER": "unknown",
            "ALGCLIENT": "cli",
            "ALGTEXT": "Unmatched event",
            "PARAM1": "unknown",
            "PARAM2": "N/A",
            "ALGSYSTEM": "misc"
        }
    ]

    # Mock read_from_stdin to simulate live input
    writer = RotatingStreamWriter(subdir="test_stream_output")
    with patch("vatrix.pipeline.stream_runner.read_from_stdin", return_value=iter(test_logs)):
        process_stream(write_output=True, writer=writer)

    # Check that files got created
    stream_dir = get_output_path("dummy.csv", subdir="test_stream_output").parent
    files = list(stream_dir.glob("*.csv"))
    assert any("streamed_logs" in f.name for f in files), "No streamed logs written."

    print("✅ End-to-end stream test passed.")

if __name__ == "__main__":
    test_end_to_end_stream()
