import timeit

from tables.list_generators import get_list_of_items, get_list_with_string_keys, get_item_of_interest, get_list_of_random_items
from indexes.naive_index import NaiveIndex
from indexes.bitmap_index import BitmapIndex
from indexes.btree import BTree
from indexes.hash_index import HashIndex

# generate a list L of items with len(L) = 20 000
# each item has a key() and data() methods
list_size = 20000
# a_long_list = get_list_of_items(list_size)
a_long_list = get_list_with_string_keys(list_size)

# a random item from the list (L.index(item) > len(L) / 2)
item_of_interest = get_item_of_interest(a_long_list)
print("Random item: ({0}, {1})".format(item_of_interest.key(), item_of_interest.value()))

print("\n =============== Naive Search =============== ")

naive_index = NaiveIndex(a_long_list)

# measure naive time
start = timeit.default_timer()
found_item = naive_index.look_up(item_of_interest)
t_no_idx = timeit.default_timer() - start
# end measure naive time

print("Elapsed time for Loop: {}".format(t_no_idx))
print("Got item: ({0}, {1})".format(found_item.key(), found_item.value()))


print("\n =============== Bitmap Index =============== ")

bitmap_index = BitmapIndex(a_long_list)

# measure index lookup term
start = timeit.default_timer()
found_items = bitmap_index.look_up(item_of_interest)
t_bitmap_idx = timeit.default_timer() - start
# end measure index lookup term

print("Elapsed time for Bitmap index: {}".format(t_bitmap_idx))
print("Faster than Naive Search in {:.2f} times".format(t_no_idx/t_bitmap_idx))

for item in found_items:
    print("Got item: ({0}, {1})".format(item.key(), item.value()))


print("\n =============== BTree Index  =============== ")

btree_index = BTree(a_long_list)

# measure index lookup term
start = timeit.default_timer()
found_item = btree_index.look_up(item_of_interest.key())
t_btree_idx = timeit.default_timer() - start
# end measure index lookup term

print("Elapsed time for Btree index: {}".format(t_btree_idx))
print("Faster than Naive Search in {:.2f} times".format(t_no_idx/t_btree_idx))

print("Got item: ({0}, {1})\n".format(found_item.key, found_item.value))
print("Let's try to generate new item of interest.")
new_item_of_interest = get_item_of_interest(a_long_list)
print("Random item: ({0}, {1})".format(new_item_of_interest.key(), new_item_of_interest.value()))
print("Now let's try to remove it from tree and find again.")
found = btree_index.look_up(new_item_of_interest.key())
print("Got item: ({0}, {1}).".format(found.key, found.value))
btree_index._delete(new_item_of_interest.key())
print("Deletion of ({0}, {1}).".format(new_item_of_interest.key(), new_item_of_interest.value()))
print("Search ({0}, {1}) again.".format(new_item_of_interest.key(), new_item_of_interest.value()))
found = btree_index.look_up(new_item_of_interest.key())
try:
    print("Got item: ({0}, {1})".format(found.key, found.value))
except:
    print("Got item: " + str(found))


print("\n =============== Hash Index =============== ")

hash_index = HashIndex(a_long_list)

# measure index lookup term
start = timeit.default_timer()
found_items = hash_index.look_up(item_of_interest)
t_hash_idx = timeit.default_timer() - start
# end measure index lookup term

print("Elapsed time for Hash index: {}".format(t_hash_idx))
print("Faster than Naive Search in {:.2f} times".format(t_no_idx/t_hash_idx))

for item in found_items:
    print("Got item: ({0}, {1})".format(item.key(), item.value()))
