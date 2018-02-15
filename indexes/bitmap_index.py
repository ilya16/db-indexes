from ctypes import *
from math import ceil
import timeit


class BitmapIndex:
    def __init__(self, initial_table, compression=True):
        self.compression = compression
        self.bitmap_table = dict()
        self.initial_table = initial_table
        self.build_index(initial_table)

    def look_up(self, item):
        result = []
        id_set = self.bitmap_table[item.key()].get_row_ids()
        for rid in id_set:
            result.append(self.initial_table[rid])
        return result

    def build_index(self, table):
        """Takes table/list/attribute and builds index, which consists of dictionary: Attribute Value => Bitmap."""
        attribute_cardinality = len(table)

        start = timeit.default_timer()
        for rid, element in enumerate(table):
            if element.key() in self.bitmap_table:
                self.bitmap_table[element.key()].set_bit(rid)
            else:
                self.bitmap_table[element.key()] = Bitmap(attribute_cardinality)
                self.bitmap_table[element.key()].set_bit(rid)

        elapsed = timeit.default_timer() - start
        print("Built Bitmap in: {}".format(elapsed))


class Bitmap:
    """ Bitmap class defines structure that maintains bit array and operations on it."""
    def __init__(self, cardinality):
        self.word_size = 32
        self.cardinality = cardinality  # number of rows of input table/list
        self.bit_array = (c_uint32 * ceil(cardinality / self.word_size))()  # define array of 32-bit unsigned integers

    def get_row_ids(self):
        """Get Row ID's where bit is set to 1."""
        # return [i for i in range(0, self.cardinality) if self.test_bit(i) == 1]
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
        """Set k-th bit to 1."""
        i = k // 32  # index in actual array of 32-bit unsigned integers
        pos = k % 32  # position of k-th bit relative to c_uint32 array element

        flag = 1
        flag = flag << pos  # set flag bit to k-th bit relative position

        self.bit_array[i] = self.bit_array[i] | flag

    def clear_bit(self, k):
        """Set k-th bit to 0."""
        i = k // 32
        pos = k % 32

        flag = 1
        flag = flag << pos
        flag = ~flag

        self.bit_array[i] = self.bit_array[i] & flag

    def test_bit(self, k):
        """Return k-th bit value."""
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
        """Define logical OR(|) operator for objects of type Bitmap."""
        product = Bitmap(self.cardinality)
        for i in range(0, len(self.bit_array)):
            product.bit_array[i] = self.bit_array[i] | other.bit_array[i]
        return product

    def __and__(self, other):
        """Define logical AND(&) operator for objects of type Bitmap."""
        product = Bitmap(self.cardinality)
        for i in range(0, len(self.bit_array)):
            product.bit_array[i] = self.bit_array[i] & other.bit_array[i]
        return product

    def __invert__(self):
        """Define logical NOT(~) operator for objects of type Bitmap."""
        product = Bitmap(self.cardinality)
        for i in range(0, len(self.bit_array)):
            product.bit_array[i] = ~self.bit_array[i]
        return product

    def to_string(self):
        """Print bit array as a string."""
        acc = ''
        for i in range(0, self.cardinality):
            acc += str(self.test_bit(i))
        print(acc)

