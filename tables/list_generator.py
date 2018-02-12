from random import randint
from .item import Item


def get_long_list_of_items(list_size):
    """Populate list with data."""
    item_list = []
    for i in range(0, list_size):
        if i % 3 == 0:
            item_list.append(Item(i, "Programming"))
        elif i % 3 == 0:
            item_list.append(Item(i, "Sports"))
        else:
            item_list.append(Item(i, "Music"))
    return item_list


def get_item_of_interest(list_of_items):
    """Pick random element from right half of list."""
    rand_index = randint(int(len(list_of_items) / 2), len(list_of_items))
    print("Randomed item: ({0}, {1})".format(list_of_items[rand_index].key(), list_of_items[rand_index].value()))
    return list_of_items[rand_index]
