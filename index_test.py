import timeit

import tables.list_generators as lstgen
from tables.item import Item
from indexes.naive_index import NaiveIndex
from indexes.bitmap_index import BitmapIndex
from indexes.btree import BTree
from indexes.hash_index import HashIndex


def build_indexes(table, index_classes):
    """
    Builds indexes for table from the index_classes dict
    :param table:           table of data
    :param index_classes:   dict of index_classes
    :return:                dictionary of built indexes
    """
    indexes = {}

    for index_name in index_classes:
        print("Building {} Index...".format(index_name))

        # measuring built time
        start = timeit.default_timer()
        index = index_classes[index_name](table)
        built_time = timeit.default_timer() - start

        print("Built {} Index in: {:.7f} s".format(index_name, built_time))
        print()

        indexes[index_name] = index

    return indexes


def test_search(indexes, table, item_of_interest):
    """
    Tests search capabilities of given indexes
    :param indexes:             a dictionary of indexes
    :param table:               table for which indexes are built
    :param item_of_interest:    searchable item
    """
    print("\n\t\tTesting search...")
    naive_index_time = None
    for index_name in indexes:
        print("\n =============== {:^6} Index =============== ".format(index_name))

        index = indexes[index_name]

        # measuring search time
        start = timeit.default_timer()
        row_ids = index.look_up(item_of_interest.key())
        search_time = timeit.default_timer() - start

        print("Elapsed time for {}: {:.7f} s".format(index_name, search_time))

        if isinstance(index, NaiveIndex):
            naive_index_time = search_time
        else:
            factor = naive_index_time / search_time
            print("Faster than Naive Search in {:.2f} times".format(naive_index_time / search_time))
            assert factor >= 1.0, "Index is slower than Naive Search, what a shame :("

        print("Found {} item(-s)".format(len(row_ids)))
        for rid in row_ids:
            item = table[rid]
            print("Got item: ({0}, {1})".format(item.key(), item.value()))


def test_insertion(indexes, table, new_item):
    """
    Tests deletion capabilities of given indexes
    :param indexes:             a dictionary of indexes
    :param table:               table for which indexes are built
    """
    print("\n\t\tTesting insertion...")
    print("Item to be inserted: ({0}, {1})".format(new_item.key(), new_item.value()))

    print("Let's check whether the indexes contain the item with the same key.")
    print("And then insert it and retrieve again.")
    table.append(new_item)

    for index_name in indexes:
        print("\n =============== {:^6} Index =============== ".format(index_name))

        index = indexes[index_name]

        print("Trying to find ({0}, {1}) in the current index.".format(new_item.key(), new_item.value()))
        row_ids = index.look_up(new_item.key())
        if row_ids:
            print("Found {} item(-s)".format(len(row_ids)))
            for rid in row_ids:
                item = table[rid]
                print("Got item: ({0}, {1})".format(item.key(), item.value()))
        else:
            print("Found 0 item(-s)")

        print("\nTrying to insert ({0}, {1}).".format(new_item.key(), new_item.value()))
        index.insert(new_item.key())
        print("Inserted. Now trying to find it")

        row_ids = index.look_up(new_item.key())
        items = [table[rid] for rid in row_ids]
        print("Found {} item(-s)".format(len(row_ids)))
        for rid in row_ids:
            item = table[rid]
            print("Got item: ({0}, {1})".format(item.key(), item.value()))

        if new_item in items:
            print("Insertion was successful!")
        else:
            print("Oops, item was not inserted...")


def test_deletion(indexes, table):
    """
    Tests deletion capabilities of given indexes
    :param indexes:             a dictionary of indexes
    :param table:               table for which indexes are built
    """
    print("\n\t\tTesting deletion...")
    print("Let's try to generate a new item of interest.")
    new_item_of_interest = lstgen.get_item_of_interest(table)
    print("Random item: ({0}, {1})".format(new_item_of_interest.key(), new_item_of_interest.value()))

    print("Now let's try to remove it from indexes and find again.")

    for index_name in indexes:
        print("\n =============== {:^6} Index =============== ".format(index_name))

        index = indexes[index_name]

        rid = index.look_up(new_item_of_interest.key())[0]
        item = table[rid]
        print("Got item: ({0}, {1})".format(item.key(), item.value()))

        # table.delete(rid) - deleting from the table in database
        # updating index
        index.delete(rid)
        print("Deleted: ({0}, {1}).".format(new_item_of_interest.key(), new_item_of_interest.value()))
        print("Searching ({0}, {1}) again.".format(new_item_of_interest.key(), new_item_of_interest.value()))

        rid = index.look_up(new_item_of_interest.key())

        if rid:
            item = table[rid[0]]
            assert rid, "Oops... Got item: ({0}, {1})".format(item.key(), item.value())
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

    print("Generated list L of {} items".format(len(lst)))
    print("Random item: ({0}, {1})\n".format(item_of_interest.key(), item_of_interest.value()))

    indexes_classes = {
        'Naive': NaiveIndex,
        'Bitmap': BitmapIndex,
        'BTree': BTree,
        'Hash': HashIndex
    }

    indexes = build_indexes(lst, indexes_classes)

    test_search(indexes, lst, item_of_interest)

    test_insertion(indexes, lst, Item("advanced databases", "db indexes are cool"))

    test_deletion(indexes, lst)
