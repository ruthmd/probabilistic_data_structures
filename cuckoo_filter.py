import mmh3
import random

class CuckooFilter:
    def __init__(self, size, bucket_size=4, max_kicks=500):
        self.size = size
        self.bucket_size = bucket_size
        self.max_kicks = max_kicks
        self.buckets = [[] for _ in range(size)]
    
    def _hash(self, item, seed):
        return mmh3.hash(item, seed) % self.size

    def _fingerprint(self, item):
        return str(mmh3.hash(item) % (2 ** 16))

    def _get_alternate_index(self, index, fingerprint):
        return (index ^ self._hash(fingerprint, 0)) % self.size

    def insert(self, item):
        fingerprint = self._fingerprint(item)
        i1 = self._hash(item, 1)
        i2 = self._get_alternate_index(i1, fingerprint)

        if len(self.buckets[i1]) < self.bucket_size:
            self.buckets[i1].append(fingerprint)
            return True

        if len(self.buckets[i2]) < self.bucket_size:
            self.buckets[i2].append(fingerprint)
            return True

        index = random.choice([i1, i2])
        for _ in range(self.max_kicks):
            if len(self.buckets[index]) < self.bucket_size:
                self.buckets[index].append(fingerprint)
                return True
            
            evict_index = random.randint(0, self.bucket_size - 1)
            fingerprint, self.buckets[index][evict_index] = self.buckets[index][evict_index], fingerprint
            index = self._get_alternate_index(index, fingerprint)

        return False  # Filter is full

    def query(self, item):
        fingerprint = self._fingerprint(item)
        i1 = self._hash(item, 1)
        i2 = self._get_alternate_index(i1, fingerprint)
        
        return fingerprint in self.buckets[i1] or fingerprint in self.buckets[i2]

    def delete(self, item):
        fingerprint = self._fingerprint(item)
        i1 = self._hash(item, 1)
        i2 = self._get_alternate_index(i1, fingerprint)
        
        if fingerprint in self.buckets[i1]:
            self.buckets[i1].remove(fingerprint)
            return True

        if fingerprint in self.buckets[i2]:
            self.buckets[i2].remove(fingerprint)
            return True

        return False  # Item not found

# Example Usage
cf = CuckooFilter(size=10**6, bucket_size=4, max_kicks=500)
cf.insert('apple')
print(f"Querying apple: {cf.query('apple')}")  # True
print(f"Querying banana: {cf.query('banana')}")  # False
cf.delete("apple")
print(f"Querying apple after deletion: {cf.query('apple')}")  # False
