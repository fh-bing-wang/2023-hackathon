import redis
import json
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

import numpy as np

class RedisServer():
    def __init__(self, redis_host, redis_port, redis_password):
        self.conn = redis.Redis(host=redis_host, port=redis_port, password=redis_password, encoding='utf-8', decode_responses=True)
    
    def create_hash(self, patient_id, documents, embeddings, item):
        p = self.conn.pipeline(transaction=False)
        i = 0
        for doc, vector in zip(documents, embeddings):

            # embedding = json.dumps(vector["embedding"])
            embedding = np.array(vector["embedding"]).astype(np.float32).tobytes()

            word_hash = {
                "doc": doc,
                "embedding": embedding
            }
        
            # create hash
            self.conn.hset(name=f"{patient_id}:{item}_{i}", mapping=word_hash)
            i+=1
        p.execute()
    
    def create_index(self, patient_id):
        SCHEMA = [
            TextField("doc"),
            VectorField("embedding", "HNSW", {"TYPE": "FLOAT32", "DIM": 1536, "DISTANCE_METRIC": "COSINE"}),
        ]
        
        # Create the index
        try:
            # creates a RediSearch index named "{patient_id}_index"
            # extra config: the keys should be prefixed with "{patient_id}:"
            self.conn.ft("{patient_id}_index").create_index(fields=SCHEMA, definition=IndexDefinition(prefix=["{patient_id}:"], index_type=IndexType.HASH))
        except Exception as e:
            print("Index already exists")

    def query_database(self, query_vector):
        # Convert the vector to a numpy array
        query_vector = np.array(query_vector).astype(np.float32).tobytes()
        results = self._search_vectors(query_vector)

        related_tokens = []
        if results:
            print(f"Found {results.total} results:")
            for i, doc in enumerate(results.docs):
                score = 1 - float(doc.vector_score)
                print(f"\t{i}. {doc} (Score: {round(score ,3) })")

                if score >= 0.6:
                    related_tokens.append(doc.doc)
        return related_tokens
    
    def _search_vectors(self, query_vector, top_k=5):
        base_query = "*=>[KNN 5 @embedding $vector AS vector_score]"
        query = Query(base_query).return_fields("word", "vector_score").sort_by("vector_score").dialect(2)    
    
        try:
            results = self.conn.ft("words").search(query, query_params={"vector": query_vector})
        except Exception as e:
            print("Error calling Redis search: ", e)
            return None
    
        return results