


class Node(object):
    """Base node object.

    Each node stores keys and values. Keys are not unique to each value, and as such values are
    stored as a list under each key.

    Attributes:
        order (int): The maximum number of keys each node can hold.
    """

    __slots__ = ('_order', '_keys', '_values', '_leaf')

    def __init__(self, order):
        """Child nodes can be converted into parent nodes by setting self.leaf = False. Parent nodes
        simply act as a medium to traverse the tree."""
        self._order = order
        self._keys = []
        self._values = []
        self._leaf = True

    def add(self, key, value):
        """Adds a key-value pair to the node."""
        # If the node is empty, simply insert the key-value pair.
        if not self._keys:
            self._keys.append(key)
            self._values.append([value])
            return None

        for i, item in enumerate(self._keys):
            # If new key matches existing key, add to list of values.
            if key == item:
                if value not in self._values[i]:
                    self._values[i].append(value)
                break

            # If new key is smaller than existing key, insert new key to the left of existing key.
            elif key < item:
                self._keys = self._keys[:i] + [key] + self._keys[i:]
                self._values = self._values[:i] + [[value]] + self._values[i:]
                break

            # If new key is larger than all existing keys, insert new key to the right of all
            # existing keys.
            elif i + 1 == len(self._keys):
                self._keys.append(key)
                self._values.append([value])

    def split(self):
        """Splits the node into two and stores them as child nodes."""
        left = Node(self._order)
        right = Node(self._order)
        mid = self._order // 2

        left._keys = self._keys[:mid]
        left._values = self._values[:mid]

        right._keys = self._keys[mid:]
        right._values = self._values[mid:]

        # When the node is split, set the parent key to the left-most key of the right child node.
        self._keys = [right._keys[0]]
        self._values = [left, right]
        self._leaf = False

    def is_full(self):
        """Returns True if the node is full."""
        return len(self._keys) == self._order

    def show(self, counter=0):
        """Prints the keys at each level."""
        print(counter, str(self._keys))

        # Recursively print the key of child nodes (if these exist).
        if not self._leaf:
            for item in self._values:
                item.show(counter + 1)

    def items(self):
        for key, values in zip(self._keys, self._values):
            if type(values).__name__ == "Node":
                yield from values.items()
            else:
                yield from [(key, value) for value in values]
        if not self._leaf:
            for item in self._values:
                yield from item.items()

    def keys(self):
        yield from self._keys
        if not self._leaf:
            for item in self._values:
                yield from item.keys()


class BPlusTree(object):
    """B+ tree object, consisting of nodes.

    Nodes will automatically be split into two once it is full. When a split occurs, a key will
    'float' upwards and be inserted into the parent node to act as a pivot.

    Attributes:
        order (int): The maximum number of keys each node can hold.
    """
    def __init__(self, order=8):
        self.root = Node(order)

    def _find(self, node, key):
        """ For a given node and key, returns the index where the key should be inserted and the
        list of values at that index."""
        for i, item in enumerate(node._keys):
            if key < item:
                return node._values[i], i

        return node._values[i + 1], i + 1

    def _merge(self, parent, child, index):
        """For a parent and child node, extract a pivot from the child to be inserted into the keys
        of the parent. Insert the values from the child into the values of the parent.
        """
        parent._values.pop(index)
        pivot = child._keys[0]

        for i, item in enumerate(parent._keys):
            if pivot < item:
                parent._keys = parent._keys[:i] + [pivot] + parent._keys[i:]
                parent._values = parent._values[:i] + child._values + parent._values[i:]
                break

            elif i + 1 == len(parent._keys):
                parent._keys += [pivot]
                parent._values += child._values
                break

    def insert(self, key, value):
        """Inserts a key-value pair after traversing to a leaf node. If the leaf node is full, split
        the leaf node into two.
        """
        parent = None
        child = self.root

        # Traverse tree until leaf node is reached.
        while not child._leaf:
            parent = child
            child, index = self._find(child, key)

        child.add(key, value)

        # If the leaf node is full, split the leaf node into two.
        if child.is_full():
            child.split()

            # Once a leaf node is split, it consists of a internal node and two leaf nodes. These
            # need to be re-inserted back into the tree.
            if parent and not parent.is_full():
                self._merge(parent, child, index)

    def retrieve(self, key):
        """Returns a value for a given key, and None if the key does not exist."""
        child = self.root

        while not child._leaf:
            child, index = self._find(child, key)

        for i, item in enumerate(child._keys):
            if key == item:
                return child._values[i]

        return None

    def show(self):
        """Prints the keys at each level."""
        self.root.show()

    def keys(self):
        yield from self.root.keys()

    def items(self):
        yield from self.root.items()

    def save(self, filename):
        import ujson as json
        with open(filename, mode='w') as file:
            for key, attributes in self.items():
                file.write(json.dumps({"key":key, "value": attributes}) + '\n')

    def load(self, filename):
        import ujson as json
        with open(filename, mode='r') as file:
            for text_line in file:
                record = json.loads(text_line)
                self.insert(record['key'], record['value'])
