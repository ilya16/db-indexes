from random import randint
from uuid import uuid4
from tables.item import Item
import csv


def generate_item_value(key):
    """
    Generates an Item value by the key.
    :param key:     key of the item
    :return:        created item
    """
    if key % 3 == 0:
        return "Programming"
    elif key % 3 == 1:
        return "Sports"
    else:
        return "Music"


def generate_item(key):
    """
    Generates an Item object by the key.
    :param key:     key of the item
    :return:        created item
    """
    return Item(key, generate_item_value(key))


def get_list_of_items(list_size):
    """
    Generates a list of items with defined data.
    :param list_size:   size of the list
    :return:            generated list of items
    """
    return [generate_item(i) for i in range(list_size)]


def get_list_of_random_items(list_size, max_number=10000):
    """
    Generates a list of items with random keys.
    :param list_size:   size of the list
    :param max_number:  the upper bound range of integer keys
    :return:            generated list of items
    """
    return [generate_item(randint(0, max_number)) for i in range(list_size)]


def get_list_with_string_keys(list_size):
    return [Item(str(uuid4()), generate_item_value(i)) for i in range(list_size)]


def get_list_from_file(path):
    with open(path, "r+") as f:
        reader = csv.reader(f)
        return [Item(row[0], row[1]) for row in reader]


def output_list_to_file(lst, path):
    with open(path, "w+") as f:
        writer = csv.writer(f)
        for item in lst:
            writer.writerow([item.key(), item.value()])


def get_item_of_interest(list_of_items, item_index=None):
    """
    Picks n element from right half of list.

    :param list_of_items:   input list with items
    :param item_index:      index of the target item (if None, random one is used)
    :return:                item of interest
    """

    if item_index is None:
        return list_of_items[randint(int(len(list_of_items) / 2), len(list_of_items) - 1)]
    else:
        return list_of_items[item_index]


if __name__ == "__main__":
    pass