
# .qx.pdb.this


Utilities for current partitioned database.

## .qx.pdb.this.getPartitions


Get all partitions of current database.
It's similar to [.Q.PV](https://code.kx.com/q/ref/dotq/#qpv-partition-values) but will return an empty list if
the database is not partitioned.

**Returns** (date[] | month[] | int[] | ()):  Partitions of the database, or an empty list
if the database is not a partitioned database.


**See also:**

[.qx.pdb.getPartitions](../pdb.md#qxpdbgetpartitions), [.qx.pdb.this.getModifiedPartitions](#qxpdbthisgetmodifiedpartitions)

## .qx.pdb.this.getModifiedPartitions


Get all partitions of current database, subject to modification by [`.Q.view`](https://code.kx.com/q/ref/dotq/#qview-subview).
It's similar to [.Q.pv](https://code.kx.com/q/ref/dotq/#qpv-modified-partition-values) but will return an empty list
if the database is not partitioned.

**Returns** (date[] | month[] | int[] | ()):  Partitions of the database subject to modification by `.Q.view`,
or an empty list if the database is not partitioned.


**See also:**

[.qx.pdb.this.getPartitions](#qxpdbthisgetpartitions)

## .qx.pdb.this.getPartitionField


Get partition field of the current database.
It's similar to [.Q.pf](https://code.kx.com/q/ref/dotq/#qpf-partition-field) but will return a null symbol if
the database is not partitioned.

**Returns** (symbol):  Partition field of the database, either of ``#!q `date`month`year`int ``, or a null symbol
if the database is not a partitioned database.


**See also:**

[.qx.pdb.getPartitionField](../pdb.md#qxpdbgetpartitionfield)

## .qx.pdb.this.getPartitionedTables


Get partitioned tables of the current database.
It's similar to [.Q.pt](https://code.kx.com/q/ref/dotq/#qpt-partitioned-tables) but will return an empty symbol vector
if the database is not partitioned.

**Returns** (symbol[]):  Partitioned tables of the database, or empty symbol vector if the database is not a partitioned database.

## .qx.pdb.this.getSegments


Get all segments.
It's similar to [.Q.P](https://code.kx.com/q/ref/dotq/#qp-segments) but will return an empty list
if the database is not partitioned.

**Returns** (hsym[] | ()):  Segments of the database, or an empty list
if the database is not a partitioned database.

## .qx.pdb.this.getPartitionsPerSegment


Partitions per segment.

**Returns** (dict):  A dictionary from segments to partitions in each segment. It's empty if the database doesn't contain
any segment.

## .qx.pdb.this.countPerPartition


Count rows of a table per partition, subject to modification by [`.Q.view`](https://code.kx.com/q/ref/dotq/#qview-subview).

**Parameter:**

1. `tableName` (symbol):  A partitioned table by name.


**Returns** (dict):  A dictionary from partitions to row count of the table in each partition.


**Throws:**

1. NotAPartitionedTableError:  If the table is not a partitioned table.

## .qx.pdb.this.countAllPerPartition


Count rows of all tables per partition.

**Returns** (dict):  A table keyed by partition and each column is row count of a partitioned table in each partition.


**Throws:**

1. RuntimeError: no partition:  If there is no partition.
