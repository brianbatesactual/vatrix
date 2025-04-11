# vatrix/api/receiver.py

import os
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from vatrix.pipeline.stream_runner import process_api_ingest

API_TOKEN = os.getenv("VATRIX_API_TOKEN", "changeme")  # Set this in env
app = FastAPI()


@app.post("/ingest/splunk")
async def ingest_event(request: Request):
    token = request.headers.get("X-Vatrix-Token")
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = await request.json()
        event = payload.get("event", {})

        row = {
            "timestamp": datetime.utcnow().isoformat(),
            "host": payload.get("host", "unknown"),
            "index": payload.get("index", "unspecified"),
            "sourcetype": payload.get("sourcetype", "unspecified"),
            "source": "vatrix:api:ingest:splunk",
            **event,
        }

        process_api_ingest(row)

        return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
