
# .qx.pdb


Utilities for partitioned database

## .qx.pdb.getPartitions


Get all partitions of a database.

**Parameter:**

1. `dbDir` (hsym):  DB directory.


**Returns** (date[] | month[] | int[] | ()):  Partitions of the database, or an empty list
if the database is not a partitioned database.


**Throws:**

1. FileNotFoundError:  If `dbDir` doesn't exist.
1. NotADirectoryError:  If `dbDir` doesn't point to a directory.

## .qx.pdb.getPartitionField


Get partition field of a database under a directory.

**Parameter:**

1. `dbDir` (hsym):  A database directory.


**Returns** (symbol):  Partition field of the database, either of ``#!q `date`month`year`int ``, or an empty symbol
if the database is not a partitioned database.


**See also:**

[.qx.pdb.this.getPartitionField](../this.md#qxpdbthisgetpartitionfield)

## .qx.pdb.fillTables


Fill all tables missing in some partitions, using the most recent partition as a template.
A rename of [`.Q.chk`](https://code.kx.com/q/ref/dotq/#qchk-fill-hdb).

**Parameter:**

1. `dbDir` (hsym):  Database directory.


**Returns** (any[]):  Partitions that are filled with missing tables.

## .qx.pdb.saveToPartition


Save table to a partition.

**Parameter:**

1. `dir` (hsym):  A directory handle.
1. `partition` (date | month | int):  A partition.
1. `tableName` (symbol):  Table name.
1. `tableData` (table):  A table of data.
1. `options` (dict (enum: dict | symbol)):  Saving options.
  - enum: a single domain for all symbol columns, or a dictionary between column names and their respective domains where the default domain is sym


**Returns** (hsym):  The path to the table in the partition.


**Throws:**

1. SchemaError:  If column names/types in the data table don't match those in the on-disk table (if exists).


**See also:**

[`.Q.dpft`](https://code.kx.com/q/ref/dotq/#qdpft-save-table)
