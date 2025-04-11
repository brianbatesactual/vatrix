# Embedding Pipeline

## Feature
Transform log events into vector embeddings using Sentence-BERT (SBERT) to enable semantic search and ML-based classification.

## Purpose
- Enable similarity search via Qdrant
- Support downstream training and fine-tuning
- Provide natural language representations of rendered log events

## How It Works
1. Log is matched to a template and rendered into a human-readable sentence.
2. The `EmbeddingPipeline` encodes the sentence using `sentence-transformers` with the `all-MiniLM-L6-v2` model.
3. The resulting 384-dimension float vector is included in the Qdrant upsert payload.

## Design Choices
- SBERT chosen for compact model size and balance of speed + quality
- Sentence embeddings are only generated from rendered templates — raw logs are excluded from embedding
- Model is loaded once and cached per process

## Limitations
- No batching yet (encode_batch exists but unused)
- No multi-model support
- Vector size is fixed at 384 dims

## Future Work
- Add support for alternative models (e.g., domain-specific finetuned SBERT)
- Move to batch inference pipeline for throughput
- Include LLM embeddings for contrastive search or annotation

## Related Modules
