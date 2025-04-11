# vatrix/config/settings.py

import os

from dotenv import load_dotenv

load_dotenv()

VATRIX_API_TOKEN = os.getenv("VATRIX_API_TOKEN", "changeme123")
GATEWAY_BASE_URL = os.getenv("GATEWAY_BASE_URL", "https://localhost:443")
GATEWAY_VERIFY_TLS = os.getenv("GATEWAY_VERIFY_TLS", "false").lower() == "true"
DEBUG_MODE = os.getenv("VATRIX_DEBUG", "false").lower() == "true"

# Compose known endpoints
GATEWAY_INGEST_URL = f"{GATEWAY_BASE_URL}/api/v1/ingest"
GATEWAY_SEARCH_URL = f"{GATEWAY_BASE_URL}/api/v1/search"
