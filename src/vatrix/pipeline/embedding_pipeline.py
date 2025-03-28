from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingPipeline:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, sentence: str) -> np.ndarray:
        """
        Encodes a single sentence into a vector.
        Returns a NumPy array (embedding vector).
        """
        return self.model.encode(sentence, convert_to_numpy=True)

    def encode_batch(self, sentences: list[str]) -> list[np.ndarray]:
        """
        Encodes a list of sentences into a list of vectors.
        """
        return self.model.encode(sentences, convert_to_numpy=True)
