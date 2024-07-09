import mmh3
import math

class HyperLogLog:
    def __init__(self, b):
        self.b = b
        self.m = 1 << b  # Number of registers
        self.data = [0] * self.m

    def add(self, item):
        # Hash the item and update the register
        x = mmh3.hash(item)
        j = x & (self.m - 1)
        w = x >> self.b
        self.data[j] = max(self.data[j], self._rho(w))

    def _rho(self, w):
        # Calculate the rank of the binary representation
        return len(bin(w)) - len(bin(w).rstrip('0')) + 1

    def count(self):
        # Calculate the estimated cardinality
        alpha = 0.7213 / (1 + 1.079 / self.m)
        Z = 1 / sum(2 ** -reg for reg in self.data)
        E = alpha * self.m ** 2 * Z
        if E <= 2.5 * self.m:
            V = self.data.count(0)
            if V > 0:
                E = self.m * math.log(self.m / V)
        elif E > 1 / 30:
            E = -self.m * math.log(1 - E / self.m)
        return int(E)

# Example Usage
hll = HyperLogLog(14)
hll.add("apple")
print(hll.count())  # Approximate cardinality
