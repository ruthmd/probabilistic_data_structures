import mmh3
import numpy as np

class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width
        self.depth = depth
        self.table = np.zeros(width * depth, dtype=int)

    def _get_index(self, item, i):
        # Compute the index in the flattened table array
        return mmh3.hash(item, i) % self.width + i * self.width

    def add(self, item):
        # Increment the counters at hashed positions
        for i in range(self.depth):
            index = self._get_index(item, i)
            self.table[index] += 1

    def query(self, item):
        # Get the minimum count from the hashed positions
        min_count = float('inf')
        for i in range(self.depth):
            index = self._get_index(item, i)
            min_count = min(min_count, self.table[index])
        return min_count

# Example Usage
cms = CountMinSketch(10**6, 10)
cms.add('apple')
print(f"Querying apple: {cms.query('apple')}")  # Approximate count
