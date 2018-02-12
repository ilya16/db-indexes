from random import randint
from .item import Item


def get_long_list_of_items(list_size):
    """ Generates a list with defined data. """
    item_list = []
    for i in range(list_size):
        if i % 3 == 0:
            item_list.append(Item(i, "Programming"))
        elif i % 3 == 1:
            item_list.append(Item(i, "Sports"))
        else:
            item_list.append(Item(i, "Music"))
    return item_list


def get_list_of_random_items(list_size, max_number=10000):
    """ Generates a list with random keys. """
    item_list = []
    for i in range(list_size):
        key = randint(0, max_number)
        if key % 3 == 0:
            item_list.append(Item(key, "Programming"))
        elif key % 3 == 1:
            item_list.append(Item(key, "Sports"))
        else:
            item_list.append(Item(key, "Music"))
    return item_list


def get_item_of_interest(list_of_items, item_index=None):
    """
    Picks n element from right half of list.

    :param list_of_items:   input list with items
    :param item_index:      index of the target item (if None, random one is used)
    :return:                item of interest
    """

    if not item_index:
        return list_of_items[randint(int(len(list_of_items) / 2), len(list_of_items))]
    else:
        return list_of_items[item_index]
