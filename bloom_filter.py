import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, item):
        # Insert item into the Bloom filter by setting bits at hashed positions
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            self.bit_array[digest] = True

    def query(self, item):
        # Check if item is in the Bloom filter
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if not self.bit_array[digest]:
                return False  # Definitely not in the set
        return True  # Probably in the set

# Example Usage
bloom = BloomFilter(10**7, 7)
bloom.add('apple')
bloom.add('mango')
bloom.add('grapes')
print(f"Querying apple: {bloom.query('apple')}")  # True
print(f"Querying banana: {bloom.query('banana')}")  # False
