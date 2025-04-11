import logging

from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

_model = SentenceTransformer("all-MiniLM-L6-v2")  # runs locally


def embed_sentence(sentence: str) -> list[float]:
    try:
        embedding = _model.encode(sentence, convert_to_numpy=True).tolist()
        logger.debug(f"Generated embedding of length {len(embedding)}")
        return embedding
    except Exception as e:
        logger.exception("Failed to embed sentence.")
        raise e
