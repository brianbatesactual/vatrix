from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, CollectionStatus
import uuid
import logging
import threading
import atexit

logger = logging.getLogger(__name__)

class QdrantWriter:
    def __init__(self, host="localhost", port=6333, collection_name="vatrix_logs"):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.batch_size = batch_size
        self.buffer = []
        self.buffer_lock = threading.Lock()
        self._ensure_collection()
        atexit.register(self.flush)

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if self.collection_name not in [c.name for c in collections]:
            logger.info(f"Creating new Qdrant collection: {self.collection_name}")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )

    def add_to_buffer(self, vector, payload):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector.tolist(),
            payload=payload
        )

        with self._buffer_lock:
            self._buffer.append(point)
            if len(self._buffer) >= self.batch_size:
                self.flush()

    def flush(self):
        with self._buffer_lock:
            if not self._buffer:
                return
    
    def upsert(self, vector, payload):
        """
        Inserts a vector with metadata (payload) into Qdrant.
        """
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector.tolist(),
            payload=payload
        )
        self.client.upsert(collection_name=self.collection_name, points=[point])
