from ctypes import *
from math import ceil
import timeit


class BitmapIndex:
    """Implements Uncompressed Bitmap Index."""
    def __init__(self, table):
        """
        Hash Index constructor.
        :param table:           table with items (rows) upon which index is built
        """
        self.bitmap_table = dict()
        self.keys = [item.key() for item in table]
        self.build_index(table)

    def look_up(self, key):
        """
        Returns a list of row ids in the table matching the  key
        :param key:     interest of search
        :return:        list of row ids matching items
        """
        if key not in self.bitmap_table:
            return None
        return self.bitmap_table[key].get_row_ids()

    def build_index(self, table):
        """
        Takes table/list/attribute and builds index
        :param table:   table with items (rows) upon which index is built
        :return:
        """
        attribute_cardinality = len(table)
        for rid, element in enumerate(table):
            if element.key() in self.bitmap_table:
                self.bitmap_table[element.key()].set_bit(rid)
            else:
                self.bitmap_table[element.key()] = Bitmap(attribute_cardinality)
                self.bitmap_table[element.key()].set_bit(rid)

    def insert(self, *keys):
        """
        Inserts information about new items in the table to the index.
        :param keys:    key of inserted item
        :return:
        """
        for key in keys:
            self.keys.append(key)
            ref_key = self.keys[0]
            if len(self.keys) == (len(self.bitmap_table[ref_key].bit_array) * self.bitmap_table[ref_key].word_size)+1:
                for bitmap in self.bitmap_table.values():
                    bitmap.cardinality += 1
                    bitmap.resize()
            else:
                for bitmap in self.bitmap_table.values():
                    bitmap.cardinality += 1

            if key in self.bitmap_table:
                self.bitmap_table[key].set_bit(len(self.keys)-1)
            else:
                self.bitmap_table[key] = Bitmap(len(self.keys))
                self.bitmap_table[key].set_bit(len(self.keys)-1)

    def delete(self, rid):
        """
        Delete element information from bitmap index
        :param rid:     row id of table that we want to update
        :return:
        """
        old_key = self.keys[rid]

        flag = Bitmap(len(self.keys))
        flag.set_bit(rid)

        if old_key in self.bitmap_table:
            xor = self.bitmap_table[old_key] ^ flag
            if xor.is_empty():
                del self.bitmap_table[old_key]
            else:
                self.bitmap_table[old_key] = xor

    def update(self, rid, key):
        """
        Updates values of item at tid in the table and the index.
        :param rid:         row id of table that we want to update
        :param key:         new item that we want to insert into row
        :return:
        """
        old_key = self.keys[rid]
        if old_key == key:
            self.keys[rid] = key
        else:
            flag = Bitmap(len(self.keys))
            flag.set_bit(rid)

            xor = self.bitmap_table[old_key] ^ flag
            if xor.is_empty():
                del self.bitmap_table[old_key]
            else:
                self.bitmap_table[old_key] = xor
            if key in self.keys:
                self.bitmap_table[key] |= flag
            else:
                self.bitmap_table[key] = Bitmap(len(self.keys))
                self.bitmap_table[key] |= flag
            self.keys[rid] = key


class Bitmap:
    """ Bitmap class defines structure that maintains bit array and operations on it."""
    def __init__(self, cardinality):
        """
        Bitmap constructor.
        :param cardinality:     Number of rows in attribute/table
        """
        self.word_size = 32
        self.cardinality = cardinality  # number of rows of input table/list
        self.bit_array = (c_uint32 * ceil(cardinality / self.word_size))()  # define array of 32-bit unsigned integers

    def get_row_ids(self):
        """
        Get Row ID's where bit is set to 1.
        :return:    list of row_ids retrieved from bitmap index table
        """
        rids = []
        for i in range(0, len(self.bit_array)):
            word = self.bit_array[i]
            if word == 0:
                continue
            for b in range(0, self.word_size):
                if (word & 1) != 0:
                    rids.append(self.word_size*i+b)
                word = word >> 1
        return rids

    # Bit manipulation in bit array
    def set_bit(self, k):
        """
        Set k-th bit to 1.
        :param k:   k-th bit
        :return:
        """
        i = k // 32  # index in actual array of 32-bit unsigned integers
        pos = k % 32  # position of k-th bit relative to c_uint32 array element

        flag = 1
        flag = flag << pos  # set flag bit to k-th bit relative position

        self.bit_array[i] = self.bit_array[i] | flag

    def clear_bit(self, k):
        """
        Set k-th bit to 0.
        :param k:   k-th bit
        :return:
        """
        i = k // 32
        pos = k % 32

        flag = 1
        flag = flag << pos
        flag = ~flag

        self.bit_array[i] = self.bit_array[i] & flag

    def test_bit(self, k):
        """
        Return k-th bit value.
        :param k:   k-th bit
        :return:
        """
        i = k // 32
        pos = k % 32

        flag = 1
        flag = flag << pos

        if self.bit_array[i] & flag:
            return 1
        else:
            return 0

    # Bitwise logical operations for bitmap
    def __or__(self, other):
        """
        Define logical OR(|) operator for objects of type Bitmap.
        :param other:   other bitmap to which you want to apply operation
        :return:        product of operation
        """
        product = Bitmap(self.cardinality)
        for i in range(0, len(self.bit_array)):
            product.bit_array[i] = self.bit_array[i] | other.bit_array[i]
        return product

    def __xor__(self, other):
        """
        Define logical Exclusive OR(^) operator for objects of type Bitmap.
        :param other:   other bitmap to which you want to apply operation
        :return:        product of operation
        """
        product = Bitmap(self.cardinality)
        for i in range(0, len(self.bit_array)):
            product.bit_array[i] = self.bit_array[i] ^ other.bit_array[i]
        return product

    def __and__(self, other):
        """
        Define logical AND(&) operator for objects of type Bitmap.
        :param other:   other bitmap to which you want to apply operation
        :return:        product of operation
        """
        product = Bitmap(self.cardinality)
        for i in range(0, len(self.bit_array)):
            product.bit_array[i] = self.bit_array[i] & other.bit_array[i]
        return product

    def __invert__(self):
        """
        Define logical NOT(~) operator for objects of type Bitmap.
        :return:        product of operation
        """
        product = Bitmap(self.cardinality)
        for i in range(0, len(self.bit_array)):
            product.bit_array[i] = ~self.bit_array[i]
        return product

    def resize(self):
        """
        Resize the array, if the size was overflown.
        :return:
        """
        temp = Bitmap(self.cardinality)
        for i in range(0, len(self.bit_array)):
            temp.bit_array[i] = self.bit_array[i] | temp.bit_array[i]
        self.bit_array = temp.bit_array
        del temp

    def is_empty(self):
        """
        Checks whether Bitmap is empty or not.
        :return:    whether bitmap empty or not
        """
        check = 0
        for i in range(0, len(self.bit_array)):
            if self.bit_array[i] == 0:
                check += 1
        if check == len(self.bit_array):
            return True
        return False

    def to_string(self):
        """
        Print bit array as a string.
        :return:
        """
        acc = ''
        for i in range(0, self.cardinality):
            acc = str(self.test_bit(i)) + acc
        print(acc)
