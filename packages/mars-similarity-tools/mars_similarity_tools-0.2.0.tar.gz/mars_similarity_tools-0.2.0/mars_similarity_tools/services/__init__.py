import numpy as np

from mars_similarity_tools.models import SimilarityObject, SimilarityResult
from mars_similarity_tools.storages import KeyValueStorage, LocalStorage
from mars_similarity_tools.augmentation import ItemVectorizer
from mars_vectorizer_sdk import VectorGroup

from pickle import dumps, loads
from gzip import compress, decompress
from itertools import starmap, islice
from dataclasses import dataclass, field
from typing import List, Dict
from maz import fnmap
from operator import itemgetter

decompress_load = lambda x: loads(decompress(x))
compress_dump   = lambda x: compress(dumps(x))

@dataclass
class VectorSimilarityService:

    augmentor:  ItemVectorizer
    storage:    KeyValueStorage = field(default_factory=LocalStorage)

    def items(self, namespace: str) -> Dict[str, SimilarityObject]:
        return dict(
            zip(
                *fnmap(
                    lambda x: x,
                    self.storage.mget,
                )(self.storage.get(namespace))
            )
        )
    
    @property
    def namespaces(self) -> List[str]:
        return list(map(lambda x: x.replace("namespace:", ""), self.storage.keys("namespace:*")))

    def create_namespace(self, namespace: str, objects: List[SimilarityObject]) -> Dict[str, SimilarityObject]:
        
        """Stores a namespace (key) pointing to a set of car keys (values) in the key-value storage."""

        d_objects = list(map(lambda x: x.to_dict(), objects))

        # Create the car key vectors and store them in the vector storage.
        # They will be keyed on namespace + car-key-hash + augmentor and vectorizer setting hash.
        # I.e. all the variables that affect the vectorization process.
        self.augmentor(d_objects)

        # Create a hash for each car key
        obj_hashes = list(map(lambda obj: obj.sha256(), objects))

        # Store a namespace -> car-key-hashes mapping in the key-value storage.
        self.storage.set(f"namespace:{namespace}", obj_hashes)

        # Store the car-key-hash -> car-key mapping in the key-value storage.
        self.storage.mset(dict(zip(obj_hashes, d_objects)))

        return dict(zip(obj_hashes, objects))
    
    def similarity_search(self, namespace: str, obj: SimilarityObject, top: int, bias: dict = {}) -> List[SimilarityResult]:

        """Searches for similar car keys in a given namespace."""

        keys = self.storage.get(f"namespace:{namespace}")
        if keys is None:
            raise Exception(f"Namespace {namespace} does not exist.")

        # Store the car key
        self.storage.set(obj.sha256(), obj.to_dict())

        # Get the car keys
        objects = [obj.to_dict()] + self.storage.mget(keys) 

        # Vectorize car keys (cache is used if already vectorized)
        vector_groups = self.augmentor(objects)

        # Vectorize the car key and search for similar vectors in the vector storage.
        # Notice we apply the bias here to the vectors to get a weighted average of the vectors.
        vectors = np.array(
            list(
                map(
                    lambda x: x.aggregate(bias), 
                    vector_groups,
                )
            )
        )

        # Create a similarity search based on the vector groups
        # It is the norm between the given car key vectors to all other vectors
        query_result = np.linalg.norm(vectors[1:]-vectors[0], axis=1)

        return list(
            islice(
                sorted(
                    starmap(
                        lambda o, score: SimilarityResult(
                            score=score,
                            obj=obj.from_dict(o),
                        ),
                        zip(
                            objects[1:],
                            query_result
                        )
                    ),
                    key=lambda x: x.score,
                ),
                top
            ),
        )
    
    def fetch_items(self, namespace: str, cls: SimilarityObject = SimilarityObject) -> List[SimilarityObject]:
        keys = self.storage.get(f"namespace:{namespace}")
        if keys is None:
            raise Exception(f"Namespace {namespace} does not exist.")
        return list(map(cls.from_dict, self.storage.mget(keys)))
    
    def fetch_vectors(self, namespace: str) -> List[VectorGroup]:
        keys = self.storage.get(f"namespace:{namespace}")
        if keys is None:
            raise Exception(f"Namespace {namespace} does not exist.")
        return self.augmentor(self.storage.mget(keys))
