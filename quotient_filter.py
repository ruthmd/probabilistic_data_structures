import math
import hashlib

class QuotientFilter:
    def __init__(self, size):
        self.size = size
        self.q = int(math.log2(size))  # number of bits for the quotient
        self.r = 32 - self.q  # number of bits for the remainder
        self.table = [None] * size
        self.metadata = [0] * size  # 3 bits packed into an int (occupied, continuation, shifted)

    def _hash(self, item):
        h = int(hashlib.md5(item.encode()).hexdigest(), 16) & ((1 << 32) - 1)
        quotient = h >> self.r
        remainder = h & ((1 << self.r) - 1)
        return quotient, remainder

    def _set_meta(self, index, occupied, continuation, shifted):
        self.metadata[index] = (occupied << 2) | (continuation << 1) | shifted

    def _get_meta(self, index):
        meta = self.metadata[index]
        return (meta >> 2) & 1, (meta >> 1) & 1, meta & 1

    def insert(self, item):
        quotient, remainder = self._hash(item)
        index = quotient

        # Robin Hood hashing insertion
        if self.table[index] is None:
            self.table[index] = (quotient, remainder)
            self._set_meta(index, 1, 0, 0)
            return True

        # Insert with Robin Hood Hashing
        current_remainder, current_occupied, current_continuation, current_shifted = remainder, 1, 0, 0
        while True:
            meta = self._get_meta(index)
            if self.table[index] is None:
                self.table[index] = (quotient, current_remainder)
                self._set_meta(index, current_occupied, current_continuation, current_shifted)
                return True

            current_remainder, self.table[index] = self.table[index][1], (quotient, current_remainder)
            current_occupied, current_continuation, current_shifted = (
                self._get_meta(index)[0], current_occupied | self._get_meta(index)[1], self._get_meta(index)[0]
            )
            index = (index + 1) % self.size

    def query(self, item):
        quotient, remainder = self._hash(item)
        index = quotient

        # Query the quotient filter
        while self.table[index] is not None:
            q, r = self.table[index]
            if q != quotient:
                return False
            if r == remainder:
                return True
            index = (index + 1) % self.size

        return False

    def delete(self, item):
        quotient, remainder = self._hash(item)
        index = quotient

        # Find and delete the item
        while self.table[index] is not None:
            q, r = self.table[index]
            if q != quotient:
                return False
            if r == remainder:
                self.table[index] = None
                self._set_meta(index, 0, 0, 0)
                return True
            index = (index + 1) % self.size

        return False

# Example Usage
qf = QuotientFilter(size=1024)
qf.insert("apple")
print(f"Querying apple: {qf.query('apple')}")  # True
print(f"Querying banana: {qf.query('banana')}")  # False
qf.delete("apple")
print(f"Querying apple after deletion: {qf.query('apple')}")  # False
