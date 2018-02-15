import timeit

import tables.list_generators as lstgen
from indexes.naive_index import NaiveIndex
from indexes.bitmap_index import BitmapIndex
from indexes.btree import BTree
from indexes.hash_index import HashIndex


def test_indexes(indexes, table, item_of_interest):
    naive_index_time = None
    for index_name in indexes:
        print("\n =============== {:^6} Index =============== ".format(index_name))

        # measuring search time
        start = timeit.default_timer()
        row_ids = indexes[index_name].look_up(item_of_interest.key())
        search_time = timeit.default_timer() - start

        print("Elapsed time for {}: {:.7f}".format(index_name, search_time))

        if index_name == 'Naive':
            naive_index_time = search_time
        else:
            print("Faster than Naive Search in {:.2f} times".format(naive_index_time / search_time))

        print("Found {} item(-s)".format(len(row_ids)))
        for rid in row_ids:
            item = table[rid]
            print("Got item: ({0}, {1})".format(item.key(), item.value()))


def test_deletion(indexes, table):
    print("Let's try to generate new item of interest.")
    new_item_of_interest = lstgen.get_item_of_interest(table)
    print("Random item: ({0}, {1})".format(new_item_of_interest.key(), new_item_of_interest.value()))

    print("Now let's try to remove it from indexes and find again.")

    for index_name in indexes:
        print("\n =============== {:^6} Index =============== ".format(index_name))

        rid = btree_index.look_up(new_item_of_interest.key())
        item = table[rid]
        print("Got item: ({0}, {1})".format(item.key(), item.value()))

        indexes[index_name].delete(new_item_of_interest.key())
        print("Deleted: ({0}, {1}).".format(new_item_of_interest.key(), new_item_of_interest.value()))
        print("Searching ({0}, {1}) again.".format(new_item_of_interest.key(), new_item_of_interest.value()))

        rid = btree_index.look_up(new_item_of_interest.key())

        if rid is not None:
            item = table[rid]
            print("Oops... Got item: ({0}, {1})".format(item.key(), item.value()))
        else:
            print("Got item: " + str(rid))
            print("Deletion was successful!")


if __name__ == "__main__":
    # reading a list L of items from the file with len(L) = 50 000
    lst = lstgen.get_list_from_file("data/test_list.csv")

    # item of interest is predefined to make reruns of tests more accurate
    item_of_interest = lstgen.get_item_of_interest(lst, item_index=40000)

    ################
    # you can also generate other lists of any size
    # list_size = 100000
    # lst = lstgen.get_list_of_items(list_size)
    # lst = lstgen.get_list_with_string_keys(list_size)

    # a random item from the list (L.index(item) > len(L) / 2)
    # item_of_interest = lstgen.get_item_of_interest(lst)
    ################

    print("Random item: ({0}, {1})".format(item_of_interest.key(), item_of_interest.value()))

    naive_index = NaiveIndex(lst)
    bitmap_index = BitmapIndex(lst)
    btree_index = BTree(lst)
    hash_index = HashIndex(lst)

    indexes = {
        'Naive': naive_index,
        'Bitmap': bitmap_index,
        'BTree': btree_index,
        'Hash': hash_index
    }

    test_indexes(indexes, lst, item_of_interest)
