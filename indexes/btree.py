#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 12:41:28 2018

@author: zytfo
"""

import math


def index_of(a_list, value):
    """ Returns an index of element in given list """
    try:
        return a_list.index(value)
    except ValueError:
        return None


class BTree:
    """ Main class of BTree index, takes list of items as a parameter and build an index on this list """
    def __init__(self, list_of_items):
        self.degree = 3
        self.root = Node()
        self.height = 0
        self.list_of_items = list_of_items
        self._insert(list_of_items)

    def split(self, node):
        """ Splitting the node if full """
        parent_node = node.parent
        if parent_node is None:
            parent_node = Node()
            self.root = parent_node
            self.height += 1

        left_node = Node()
        left_node.parent = parent_node
        left_node.add_entries(node.get_left_entries())

        right_node = Node()
        right_node.parent = parent_node
        right_node.right_most = node.right_most
        right_node.add_entries(node.get_right_entries())

        middle_entry = node.get_middle_entry()
        left_entry = node.get_middle_left_entry()
        if left_entry is not None:
            left_node.right_most = middle_entry.left

        middle_entry.left = left_node
        parent_node.add_entry(middle_entry)

        right_entry = parent_node.right_entry(middle_entry)
        if right_entry is None:
            parent_node.right_most = right_node
        else:
            right_entry.left = right_node

        for e in left_node.entries:
            if e.left is not None:
                e.left.parent = left_node

        if left_node.right_most is not None:
            left_node.right_most.parent = left_node

        for e in right_node.entries:
            if e.left is not None:
                e.left.parent = right_node

        if right_node.right_most is not None:
            right_node.right_most.parent = right_node

        if parent_node.entry_size() >= self.degree:
            self.split(parent_node)

    def insert(self, key, value, node):
        """ Inserts a key-value pair into the tree"""
        if node.right_most is None:
            node.add_entry(Entry(key, value, node))

            if node.entry_size() >= self.degree:
                self.split(node)
        else:
            index = 0
            for entry in node.entries:
                if key > entry.key:
                    index += 1
                    continue
                elif key == entry.key:
                    return
                elif key < entry.key:
                    self.insert(key, value, entry.left)
                    return

            if index >= node.entry_size():
                self.insert(key, value, node.right_most)

    def delete(self, entry):
        """ Deletes given entry from tree and rebalance it then """
        node = self.get_entry_node(entry, self.root)
        if node.right_most is None:
            node.remove_entry(entry)
            if node.entry_size() < math.ceil(self.degree / 2) and self.height is not 0:
                self.rebalance(node, entry)
        else:
            right_most = entry.left
            while right_most.right_most is not None:
                right_most = right_most.right_most
            left_largest = right_most.last_entry()
            right_most.remove_entry(left_largest)
            entry.key = left_largest.key
            entry.value = left_largest.value
            self.rebalance(right_most, left_largest)

    def get_entry_node(self, e, node):
        """ Returns a node that should be removed """
        if node is None:
            return None
        else:
            index = 0
            for entry in node.entries:
                if e.key > entry.key:
                    index += 1
                    continue
                elif e.key == entry.key:
                    return node
                elif e.key < entry.key:
                    return self.get_entry_node(e, entry.left)
            if index >= node.entry_size():
                return self.get_entry_node(e, node.right_most)
        return None

    def search(self, key, node):
        """ Searches given key in a tree """
        if node is None:
            return None
        else:
            index = 0
            for entry in node.entries:
                if key > entry.key:
                    index += 1
                    continue
                elif key == entry.key:
                    return entry
                elif key < entry.key:
                    return [self.search(key, entry.left)]
            if index >= node.entry_size():
                return [self.search(key, node.right_most)]
        return None

    def rebalance(self, node, deleted_node, ):
        """ Rebalances tree after deletion """
        separator = None
        parent_node = node.parent
        children = []
        for entry in parent_node.entries:
            if entry.left == node:
                separator = entry
            children.append(entry.left)
        if parent_node.right_most == node:
            separator = parent_node.last_entry()

        children.append(parent_node.right_most)
        index = index_of(children, node)
        if index < len(children) - 1 and children[index + 1].entry_size() > math.ceil((self.degree / 2)):
            right_siblings = children[index + 1]
            right_sibling = right_siblings.first_entry()
            right_sibling.left = separator.left
            separator.left = deleted_node.left
            node.add_entry(separator)
            parent_node.remove_entry(separator)
            parent_node.add_entry(right_sibling)
            right_siblings.remove_entry(right_sibling)
            return
        elif index > 0 and children[index - 1].entry_size() > math.ceil((self.degree / 2)):
            separator = parent_node.left_entry(separator)
            left_siblings = children[index - 1]
            left_sibling = left_siblings.last_entry()
            left_sibling.left = separator.left
            separator.left = deleted_node.left
            node.add_entry(separator)
            parent_node.remove_entry(separator)
            parent_node.add_entry(left_sibling)
            left_siblings.remove_entry(left_sibling)
            return
        else:
            new_node = Node()
            new_node.add_entries(node.entries)
            if index < len(children) - 1:
                right_siblings = children[index + 1]
                new_node.add_entries(right_siblings.entries)
                separator.left = node.right_most
                new_node.right_most = right_siblings.right_most
            elif index > 0:
                left_siblings = children[index - 1]
                new_node.add_entries(left_siblings.entries)
                separator.left = left_siblings.right_most
                if node.entry_size() > 0:
                    new_node.right_most = node.first_entry().left
                else:
                    new_node.right_most = node.right_most
            new_node.add_entry(separator)
            for e in new_node.entries:
                if e.left is not None:
                    e.left.parent = new_node
            if new_node.right_most is not None:
                new_node.right_most.parent = new_node
            new_node.parent = parent_node
            right_entry = parent_node.right_entry(separator)
            if right_entry is not None:
                right_entry.left = new_node
            else:
                parent_node.right_most = new_node
            parent_node.remove_entry(separator)

            if parent_node.entry_size() < math.ceil(self.degree / 2):
                if parent_node.parent is None:
                    new_node.parent = None
                    self.root = new_node
                    self.height -= 1
                else:
                    self.rebalance(parent_node, separator)

    def look_up(self, key):
        """ Search preparation """
        return self.search(key, self.root).value

    def _insert(self, list_of_items):
        """ Insert preparation """
        for rid, item in enumerate(list_of_items):
            self.insert(item.key(), rid, self.root)

    def _delete(self, key):
        """ Delete preparation """
        entry = self.search(key, self.root)
        self.delete(entry)


class Node:
    """ Node class, contains all entries getting methods """
    def __init__(self):
        self.entries = []
        self.parent = None
        self.right_most = None

    def add_entry(self, entry):
        """ Adds an entry into the list of entries """
        self.entries.append(entry)
        self.entries.sort(key=entry.compare_to, reverse=True)

    def first_entry(self):
        """ Returns first entry from list of entries """
        if self.entry_size() > 0:
            return self.entries[0]
        return None

    def last_entry(self):
        """ Returns last entry from list of entries """
        if self.entry_size() > 0:
            return self.entries[self.entry_size() - 1]
        return None

    def remove_entry(self, entry):
        """ Deletes an entry from list of entries """
        self.entries.remove(entry)

    def add_entries(self, entries):
        """ Adds new entries into the list of entries """
        self.entries.extend(entries)

    def entries(self):
        """ Returns list of entries """
        return self.entries

    def entry_size(self):
        """ Returns the size of list of entries """
        return len(self.entries)

    def get_left_entries(self):
        """ Returns left half of list of entries """
        return self.entries[0: self.entry_size() // 2]

    def get_right_entries(self):
        """ Returns right half of list of entries """
        return self.entries[self.entry_size() // 2 + 1: self.entry_size()]

    def get_middle_entry(self):
        """ Returns middle element from list of entries """
        return self.entries[self.entry_size() // 2]

    def get_middle_left_entry(self):
        """ Returns left middle entry from list of entries """
        return self.entries[self.entry_size() // 2 - 1]

    def get_middle_right_entry(self):
        """ Returns right middle entry from list of entries """
        return self.entries[self.entry_size() // 2 + 1]

    def left_entry(self, entry):
        """ Returns an entry to the left of a given entry """
        index = index_of(self.entries, entry)
        if index in range(1, self.entry_size()):
            return self.entries[index - 1]
        return None

    def right_entry(self, entry):
        """ Returns an entry to the right of a given entry """
        index = index_of(self.entries, entry)
        if index in range(0, self.entry_size() - 1):
            return self.entries[index + 1]
        return None


class Entry:
    """ Entry class """
    def __init__(self, key, value, cont):
        self.key = key
        self.value = value
        self.left = None

    """ Custom comparing function to compare int and strings """
    def compare_to(self, other):
        return (self.key > other.key) - (self.key < other.key)

    """ Prints entry """
    def print_entry(self):
        return "({0},{1},{2})".format(self.key, self.value, self.left)
