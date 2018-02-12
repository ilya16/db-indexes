class HashIndex:
    """ Implements Hash Index. """

    def __init__(self, table):
        """
        Hash Index constructor.
        :param table:           table with items (rows) upon which index is built
        """
        self.hash_table = HashTable()
        self.table = table
        self.build_index(table)

    def build_index(self, table):
        """
        Builds a index from the table of key-value items.
        :param table:   table with items (rows)
        """
        for tid, element in enumerate(table):
            self.hash_table.put(element.key(), tid)

    def look_up(self, item):
        """
        Returns a list of items in the table matching the item's key
        :param item:    interest of search
        :return:        list of matching items
        """
        nodes = self.hash_table.get(item.key())
        result = []

        for node in nodes:
            # checking that node's key is the needed one by referencing the table
            if self.table[node.value].key() == item.key():
                result.append(self.table[node.value])

        return result


class HashTable:

    def __init__(self, capacity=16, load_factor=0.75):
        """
        Hash Table constructor.
        :param capacity:        initial number of buckets used to store the keys
        :param load_factor:     load factor based on which hash table is resized
        """
        self.buckets = [None for i in range(capacity)]
        self.load_factor = load_factor
        self.size = 0

    class Node:
        """ Stores the hash values with corresponding TID numbers (id in the table). """
        def __init__(self, hash_code, key, value, next_node=None):
            """
            Node constructor.
            :param hash_code:   hash_code of the key
            :param key:         key of the node
            :param value:       node value
            :param next_node:   link to a next node in the bucket
            """
            self.hash_code = hash_code
            self.key = key
            self.value = value
            self.next_node = next_node

    def hash_code(self, key):
        """
        Returns a hash code for a given key.
        :param key:     str on int value
        :return:        hash code
        """
        if key is None:
            return 0
        else:
            h = hash(key)
            return h ^ (h >> 16)

    def index_for(self, h):
        return h & (len(self.buckets) - 1)

    def put(self, key, value, transfer=False):
        """
        Puts a new key-value pair to hash table.
        :param key:         key of the item
        :param value:       value
        :param transfer:    is data being transferred from old version (used in resize())
        """
        hash_code = self.hash_code(key)

        if self.size + 1 >= len(self.buckets) * self.load_factor:
            self.resize()

        index = self.index_for(hash_code)

        # first node in the corresponding bucket
        node = self.buckets[index]

        if node is not None:
            # trying to find the node with the same hash_code
            while node is not None and node.hash_code != hash_code:
                node = node.next_node

            new_node = self.Node(hash_code, key, value, node.next_node)
            node.next_node = new_node

        else:
            # no nodes in the bucket, add new Entry
            self.buckets[index] = self.Node(hash_code, key, value, None)

        if not transfer:
            self.size += 1

    def get(self, key):
        """
        Returns a list of nodes matching the hash code of the key.
        :param key:     ley
        :return:        a list of nodes
        """
        hash_code = self.hash_code(key)
        index = self.index_for(hash_code)
        node = self.buckets[index]

        if node is not None:
            while node.next_node is not None and node.hash_code != hash_code:
                node = node.next_node

            if node is None:
                return None
            else:
                result = []
                while node is not None and node.hash_code == hash_code:
                    result.append(node)
                    node = node.next_node
                return result
        else:
            return None

    def resize(self):
        """
        Doubles the capacity of the the hash table.
        """
        old_buckets = self.buckets
        self.buckets = [None for i in range(len(self.buckets) * 2)]

        for node in old_buckets:
            if node is not None:
                while node is not None:
                    self.put(node.key, node.value, transfer=True)
                    node = node.next_node

    def __str__(self):
        """
        Builds a string representation of the Hash Table
        :return:    str value
        """
        result = ""
        for i in range(len(self.buckets)):
            node = self.buckets[i]
            result += "Bucket {:2d}: ".format(i)
            if node is not None:
                while node is not None:
                    result += " [{}]({})({}) ".format(node.key, node.hash_code, node.tid)
                    node = node.next_node
            result += "\n"
        return result


if __name__ == "__main__":
    pass

