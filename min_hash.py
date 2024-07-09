import hashlib
import random
import numpy as np

class MinHash:
    def __init__(self, num_hashes):
        self.num_hashes = num_hashes
        self.hash_funcs = [self._generate_hash_func() for _ in range(num_hashes)]

    def _generate_hash_func(self):
        # Generate a hash function with a random seed
        seed = random.randint(0, 2**32 - 1)
        def hash_func(x):
            return int(hashlib.md5((x + str(seed)).encode('utf8')).hexdigest(), 16)
        return hash_func

    def signature(self, set):
        # Calculate the MinHash signature for a set
        sig = np.full(self.num_hashes, float('inf'))
        for e in set:
            for i, h in enumerate(self.hash_funcs):
                sig[i] = min(sig[i], h(e))
        return sig

    def jaccard_similarity(self, sig1, sig2):
        # Calculate the Jaccard similarity between two signatures
        assert len(sig1) == len(sig2)
        return np.sum(sig1 == sig2) / len(sig1)

# Example Usage
mh = MinHash(200)
set1 = {"apple", "banana", "cherry"}
set2 = {"banana", "cherry", "date"}
sig1 = mh.signature(set1)
sig2 = mh.signature(set2)
print(mh.jaccard_similarity(sig1, sig2))  # Approximate Jaccard similarity
