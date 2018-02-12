#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 12:41:28 2018

@author: zytfo
"""
from random import randint
import timeit
from tables.item import Item

class BTree:

    def __init__(self, list):
        self.degree = 4
        self.root = None
        self.height = 0
        self.n = 0                                        # number of key-value
        self.b_tree()
        self.upload(list)

    class Node:
        def __init__(self, k, t):
            self.number_of_children = k                   # number of children
            self.children = [None] * t

    class Entry:
        def __init__(self, key, value, next_node):
            self.key = key
            self.value = value
            self.next_node = next_node

    def b_tree(self):
        self.root = self.Node(0, self.degree)

    def get_value_by_key(self, key):
        return self.search(self.root, key, self.height)

    def search(self, x, key, height):
        children = x.children
        if height == 0:
            for j in range(0, x.number_of_children):
                if key is children[j].key:
                    return children[j]
        else:
            for j in range(0, x.number_of_children):
                if (j+1 == x.number_of_children) or (key < children[j+1].key):
                    return self.search(children[j].next_node, key, height-1)
        return None

    def look_up(self, key):
        return self.get_value_by_key(key)

    def upload(self, l):
        for element in l:
           self.put_new_element(element.key(), element.value())

    def put_new_element(self, key, value):
        new_n = self.insert(self.root, key, value, self.height)
        self.n += 1
        if new_n is None:
            return
        subnode = self.Node(2, self.degree)
        subnode.children[0] = self.Entry(self.root.children[0].key, None, self.root)
        subnode.children[1] = self.Entry(new_n.children[0].key, None, new_n)
        self.root = subnode
        self.height += 1

    def split(self, node):
        subnode = self.Node(self.degree//2, self.degree)
        node.number_of_children = self.degree//2
        for j in range(0, self.degree//2):
            subnode.children[j] = node.children[self.degree//2+j]
        return subnode

    def insert(self, node, key, value, height):
        j = 0
        flag = False
        subnode = self.Entry(key, value, None)
        if height == 0:
            for j in range(0, node.number_of_children):
                if key < node.children[j].key:
                    flag = True
                    break
            if flag is False:
                j = node.number_of_children
        else:
            for j in range(0, node.number_of_children):
                if (j+1 == node.number_of_children) or (key < node.children[j+1].key):
                    new_n = self.insert(node.children[j].next_node, key, value, height-1)
                    j += 1
                    if new_n is None:
                        return None
                    subnode.key = new_n.children[0].key
                    subnode.next_node = new_n
                    break
        for i in range(node.number_of_children, j, -1):
            node.children[i] = node.children[i-1]
        node.children[j] = subnode
        node.number_of_children += 1
        if node.number_of_children < self.degree:
            return None
        else:
            return self.split(node)

    def print_tree(self, node, height, indent):
        children = node.children
        st = ''
        if height == 0:
            for j in range(0, node.number_of_children):
                st += indent + '(' + str(children[j].key) + ' ' + str(children[j].value) + ')\n'
        else:
            for j in range(0, node.number_of_children):
                if j > 0:
                    st += indent + '<' + str(children[j].key) + '>\n'
                st += self.print_tree(children[j].next_node, height-1, indent + '      ')
        return st