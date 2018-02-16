# Database Indexes

This is a repository with implementation and comparison of 
non-clustered database indexes on Python programming language
for the assignment in Advanced Databases course at Innopolis University.

The task was to implement three indexes:
* B-Tree index
* Hash index
* Bitmap index

Source code of indexes is provided in the package [indexes](indexes).

Search capabilities of each index are compared with Naive index 
(simple for-loop search).

As a unit (row) of data in the table we use objects of class [Item](tables/item.py).
Each item has:
* a single value `key`
* a field for data called `value` which does not affect index structures, 
but used only in index tests.
 
As a test data for the indexes any lists of items can be passed. 

We provide several methods in the file [list_generators.py](tables/list_generators.py)
for generating lists of items with integer or string keys. To make tests more
determined we also provide a pregenerated file with items in the directory
[data](data).

To test the indexes run the file `index_test.py` using a Python (>=3.6) interpreter.
Default run includes construction of indexes for a table in the defined above file,
search and deletion test.

To change the configuration of tests, please, modify the code in the file
[index_test.py](index_test.py). Comments in the file display other test options.