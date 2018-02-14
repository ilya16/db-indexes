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

    def insert_item(self, item):
        """
        Inserts information about new item in the table to the index.
        :param item:    inserted item
        """
        self.table.append(item)
        self.hash_table.put(item.key(), len(self.table) - 1)

    def update_item(self, tid, item):
        """
        Updates values of item at tid in the table and the index.
        :param tid:
        :param item:
        :return:
        """
        old_item = self.table[tid]
        if old_item.key() == item.key():
            self.table[tid] = item
        else:
            self.hash_table.remove(old_item.key(), tid)
            self.hash_table.put(item.key(), tid)

    def delete_item(self, tid):
        """
        Deletes the item information from the index.
        :param tid:
        :return:
        """
        old_item = self.table[tid]
        self.hash_table.remove(old_item.key(), tid)
        # self.table.pop(tid)

    def __str__(self):
        """
        Returns a string representation of the Hash Index
        :return:    str value
        """
        return str(self.hash_table)


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
        index = self.index_for(hash_code)
        node = self._get_node(hash_code)

        if node is not None:
            if node.next_node is None:
                new_node = self.Node(hash_code, key, value, None)
            else:
                new_node = self.Node(hash_code, key, value, node.next_node)
            node.next_node = new_node

        else:
            # no nodes in the bucket, add new Entry
            self.buckets[index] = self.Node(hash_code, key, value, None)

        if not transfer:
            self.size += 1
            # resize if load of buckets has become high
            if self.size >= len(self.buckets) * self.load_factor:
                self.resize()

    def get(self, key):
        """
        Returns a list of nodes matching the hash code of the key.
        :param key:     key
        :return:        a list of nodes
        """
        hash_code = self.hash_code(key)
        node = self._get_node(hash_code)

        if node is not None:
            result = []
            while node is not None and node.hash_code == hash_code:
                result.append(node)
                node = node.next_node
            return result
        else:
            return None

    def remove(self, key, value):
        """
        Removes the node from the Hash Table.
        :param key:     key of the node
        :param value:   value of the node
        """
        hash_code = self.hash_code(key)
        index = self.index_for(hash_code)
        prev_node, node = self._get_node(hash_code, return_prev=True)

        if node is not None:
            if node is not None:
                while node is not None and node.hash_code == hash_code:
                    if node.value == value:
                        if prev_node is None:
                            # deletion of first node in the bucket
                            self.buckets[index] = node.next_node
                        else:
                            prev_node.next_node = node.next_node
                        node = None
                        self.size -= 1
                    else:
                        prev_node = node
                        node = node.next_node

        # resize if load of buckets has become low
        if self.size - 1 < len(self.buckets) * self.load_factor / 2:
            self.resize(factor=0.5)

        return

    def resize(self, factor=2.0):
        """
        Doubles the capacity of the the hash table.

        :param factor:  len(new_buckets) = len(old_buckets) * factor
        """
        old_buckets = self.buckets
        self.buckets = [None for i in range(int(len(self.buckets) * factor))]

        for node in old_buckets:
            if node is not None:
                while node is not None:
                    self.put(node.key, node.value, transfer=True)
                    node = node.next_node

    def _get_node(self, hash_code, return_prev=False):
        """
        Returns the first node in the hash table matching the hash_code
        :param hash_code:       hash_code value
        :param return_prev:     set True if you want to get the previous node
        :return:                the node matching the hash_code, or the previous one in the bucket
        """
        # first node in the corresponding bucket
        node = self.buckets[self.index_for(hash_code)]

        if node is not None:
            prev_node = None
            while node.next_node is not None and node.hash_code != hash_code:
                prev_node = node
                node = node.next_node

            return (prev_node, node) if return_prev else node
        else:
            return None

    def __str__(self):
        """
        Returns a string representation of the Hash Table
        :return:    str value
        """
        result = ""
        for i in range(len(self.buckets)):
            node = self.buckets[i]
            result += "Bucket {:2d}: ".format(i)
            if node is not None:
                while node is not None:
                    result += " [{}]({})({}) ".format(node.key, node.hash_code, node.value)
                    node = node.next_node
            result += "\n"
        return result


if __name__ == "__main__":
    pass
