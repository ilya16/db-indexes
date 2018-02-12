from ctypes import *
from math import ceil


class BitmapIndex:

    def __init__(self, initial_table):
        self.bitmap_table = dict()
        self.initial_table = initial_table
        self.build_index(initial_table)

    def lookup(self, item):
        return self.initial_table[self.bitmap_table[item].get_row_ids()[0]]

    def build_index(self, item_attribute):
        """Takes table/list/attribute and builds index, which consists of dictionary: Attribute Value => Bitmap."""
        attribute_cardinality = len(item_attribute)
        distinct_values = set(item_attribute)
        for i in distinct_values:
            self.bitmap_table[i] = Bitmap(attribute_cardinality)
            # slows down indexing a bit
            for k in range(0, len(item_attribute)):
                if i is item_attribute[k]:
                    self.bitmap_table[i].set_bit(k)


class Bitmap:
    """ Bitmap class defines structure that maintains bit array and operations on it."""
    def __init__(self, cardinality):
        self.cardinality = cardinality  # number of rows of input table/list
        self.bit_array = (c_uint32 * ceil(cardinality / 32))()  # define array of 32-bit unsigned integers

    def get_row_ids(self):
        """Get Row ID's where bit is set to 1."""
        return [i for i in range(0, self.cardinality) if self.test_bit(i) == 1]

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