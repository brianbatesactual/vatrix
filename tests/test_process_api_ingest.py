# /src/vatrix/tests/test_process_api_ingest.py
# v2 testing program

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from vatrix.pipeline.process_api_ingest import process_api_ingest

# Sample log entry to feed in
sample_log = {
    "TXSUBCLSID": "Dialog Logon",
    "ALGUSER": "DDIC",
    "ALGCLIENT": "800",
    "ALGSYSTEM": "w16s24id8606",
    "ALGDATE": "20250320",
    "ALGTIME": "125232",
    "ALGTEXT": "Logon successful (type=B, method=A)",
    "CURRENT_TIMESTAMP": 20250320015236,
}


@patch("vatrix.pipeline.process_api_ingest.send_to_gateway")
@patch("vatrix.pipeline.process_api_ingest.stream_writer.write")
def test_process_api_ingest_pipeline(mock_writer, mock_gateway):
    # Setup mock for gateway
    mock_gateway.return_value = None

    # Run the processor
    process_api_ingest(sample_log)

    # Assert writer was called with a rendered string
    mock_writer.assert_called_once()
    rendered_sentence = mock_writer.call_args[0][0]
    assert isinstance(rendered_sentence, str)
    assert "DDIC" in rendered_sentence or "client 800" in rendered_sentence

    # Assert gateway was called with expected structure
    mock_gateway.assert_called_once()
    args, kwargs = mock_gateway.call_args
    assert "project" in kwargs
    assert "embeddings" in kwargs
    assert isinstance(kwargs["embeddings"], list)
    assert len(kwargs["embeddings"]) == 1

    entry = kwargs["embeddings"][0]
    assert "id" in entry
    assert "vector" in entry
    assert isinstance(entry["vector"], list)
    assert len(entry["vector"]) in [384, 768]
    assert "payload" in entry
    assert isinstance(entry["payload"], dict)
    assert "rendered" in entry["payload"]
    assert entry["payload"]["template"] == "dialog_logon"
    assert isinstance(entry["timestamp"], datetime)
