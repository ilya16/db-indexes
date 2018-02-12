import timeit

from tables.list_generators import get_long_list_of_items, get_item_of_interest
from indexes.naive_index import NaiveIndex
from indexes.bitmap_index import BitmapIndex
from indexes.btree import BTree
from indexes.hash_index import HashIndex

# generate a list L of items with len(L) = 20 000
# each item has a key() and data() methods
list_size = 1000
a_long_list = get_long_list_of_items(list_size)

# a random item from the list (L.index(item) > len(L) / 2)
item_of_interest = get_item_of_interest(a_long_list)
print("Random item: ({0}, {1})".format(item_of_interest.key(), item_of_interest.value()))

print(" =============== Naive Search =============== ")

naive_index = NaiveIndex(a_long_list)

# measure naive time
start = timeit.default_timer()
found_item = naive_index.look_up(item_of_interest)
print("Elapsed time for Loop: {}".format(timeit.default_timer() - start))
# end measure naive time

print("Got item: ({0}, {1})".format(found_item.key(), found_item.value()))


print(" =============== Bitmap Index =============== ")

bitmap_index = BitmapIndex(a_long_list)

# measure index lookup term
start = timeit.default_timer()
found_items = bitmap_index.look_up(item_of_interest)
print("Elapsed time for Bitmap index: {}".format(timeit.default_timer() - start))
# end measure index lookup term

for item in found_items:
    print("Got item: ({0}, {1})".format(item.key(), item.value()))


print(" =============== BTree Index  =============== ")

btree_index = BTree(a_long_list)

# measure index lookup term
start = timeit.default_timer()
found_item = btree_index.look_up(item_of_interest)
print("Elapsed time for Btree index: {}".format(timeit.default_timer() - start))
# end measure index lookup term

print("Got item: ({0}, {1})".format(found_item.key, found_item.value))


print(" =============== Hash Index =============== ")

hash_index = HashIndex(a_long_list)
# hash_index.print_index()

# measure index lookup term
start = timeit.default_timer()
found_items = hash_index.look_up(item_of_interest)
print("Elapsed time for Hash index: {}".format(timeit.default_timer() - start))
# end measure index lookup term

for item in found_items:
    print("Got item: ({0}, {1})".format(item.key(), item.value()))
