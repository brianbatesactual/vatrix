# Vatrix Test Plan

Project: Vatrix NLP Processor
Version: v0.1.2
Environment: Local (staging) & Remote Ubuntu Server running OSAI-Demo Stack
Owner: Brian BatesLast 
Updated: 2025-04-09

## 1. Objective

To validate the functionality, performance, and reliability of the Vatrix NLP Processor and ensure seamless integration with the OSAI Stack handled by Vatrix Gateway. This includes ingestion, buffering, rotation, sentence generation, embedding, and vector database storage.

## 2. Scope

**In Scope**
- REST ingestion API via FastAPI
- Token-based authentication
- File buffering and rotation
- Log-to-text template rendering
- SBERT sentence pair generation
- Qdrant embedding storage
- MongoDB storage layer (optional)
- TLS/Nginx gateway (optional)

**Out of Scope**
- Frontend visualization layer
- Analytics dashboard
- Production monitoring stack

## 3. Test Categories

**A. Gateway Writer Validation**

| Test Case |           Description          |         Expected Result         |
|:---------:|:------------------------------:|:-------------------------------:|
| GW-01     | Send valid event via REST      | 200 OK, payload saved           |
| GW-02     | Send malformed JSON            | 400 Bad Request                 |
| GW-03     | Send request without token     | 401 Unauthorized                |
| GW-04     | Exceed max file size           | New file rotated                |
| GW-05     | Exceed max retention period    | Old file removed                |
| GW-06     | Simulate disk error            | Logged error, graceful failure  |
| GW-07     | High-volume test (e.g. 1k/sec) | No drops, buffered correctly    |

**B. NLP Processor Validation**

| Test Case | Description               | Expected Result                      |
|-----------|---------------------------|--------------------------------------|
| NLP-01    | Detect new log file       | File picked up by processor          |
| NLP-02    | Match log to template     | Natural language output              |
| NLP-03    | Generate SBERT pair       | CSV contains valid sentence1/2/score |
| NLP-04    | Insert vector to Qdrant   | Embedding indexed and searchable     |
| NLP-05    | Validate metadata         | Tags stored correctly in Qdrant      |
| NLP-06    | Export raw+processed logs | CSV written to training directory    |

**C. Vector Search & Recall Validation**

| Test Case | Description                  | Expected Result             |
|-----------|------------------------------|-----------------------------|
| VEC-01    | Run vector similarity query  | Top-k results returned      |
| VEC-02    | Compare sentence and results | Similar semantics retrieved |
| VEC-03    | Run invalid query            | 400 or safe fallback        |

**D. Security & Deployment**

| Test Case | Description               | Expected Result               |
|-----------|---------------------------|-------------------------------|
| SEC-01    | Use valid token           | 200 OK                        |
| SEC-02    | Use expired/invalid token | 401 Unauthorized              |
| SEC-03    | Send request via HTTPS    | Encrypted channel             |
| SEC-04    | Restart all containers    | All services come up clean    |
| SEC-05    | TLS misconfiguration      | Nginx error logged gracefully |

**E. Observability & Maintenance**

| Test Case | Description            | Expected Result                          |
|-----------|------------------------|------------------------------------------|
| OBS-01    | Logging level = INFO   | Sane, readable logs                      |
| OBS-02    | Rotate logs daily      | New log file created                     |
| OBS-03    | Send /health check     | 200 OK                                   |
| OBS-04    | Stress test memory/cpu | No crash, logs warning if over threshold |

## 4. Tooling

- Test Client: Postman, curl, k6 (for load)
- Log Inspection: tail -f, less, VSCode
- DB Validation: qdrant-client
- Metrics (optional): Prometheus scraping /metrics if added
- Automation (optional): Makefile task make validate or shell runner

## 5. Acceptance Criteria

- All functional and integration tests pass.
- No memory leaks or resource contention during high-volume tests.
- Log files and embeddings are correctly rotated and retained.
- REST and vector components are stable under restart and failure simulation.
- SBERT-generated sentence pairs are semantically valid and ready for fine-tuning.

## 6. Notes & Next Steps

- Review vatrix-processor config for parallel processing mode if scale grows.
- Consider including sentence-pair QA sampling loop for future fine-tuning UX.
- CI/CD to run GW + NLP smoke test on push to main.