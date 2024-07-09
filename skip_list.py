import random

class Node:
    def __init__(self, level, value):
        self.value = value
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level, p):
        self.max_level = max_level
        self.p = p
        self.header = self.create_node(self.max_level, -1)
        self.level = 0

    def create_node(self, level, value):
        # Create a new node with the given level and value
        return Node(level, value)

    def random_level(self):
        # Randomly determine the level of a new node
        level = 0
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level

    def insert(self, value):
        # Insert a value into the skip list
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        level = self.random_level()

        if level > self.level:
            for i in range(self.level + 1, level + 1):
                update[i] = self.header
            self.level = level

        node = self.create_node(level, value)
        for i in range(level + 1):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def search(self, value):
        # Search for a value in the skip list
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.value == value:
            return True
        return False

# Example Usage
skiplist = SkipList(16, 0.5)
skiplist.insert(3)
skiplist.insert(6)
print(skiplist.search(3))  # True
print(skiplist.search(7))  # False
