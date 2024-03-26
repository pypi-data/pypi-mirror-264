
# .qx.tbl


Utilities for table manipulations.

## .qx.tbl.getType


Get table type, either of `` `Plain`Serialized`Splayed`Partitioned ``. Note that tables in segmented database
are classified as Partitioned.

**Parameter:**

1. `t` (table | symbol | hsym | (hsym; symbol; symbol)):  Table or table reference.


**Returns** (symbol):  Table type.


**Throws:**

1. ValueError:  If `t` is a symbol vector but not a valid partitioned table ID.


**See also:**

[.Q.qp](https://code.kx.com/q/ref/dotq/#qqp-is-partitioned).

## .qx.tbl.meta


Get metadata of a table. It's similar to [meta](https://code.kx.com/q/ref/meta/) but supports all table types.
For partitioned table, the latest partition is used.

**Parameter:**

1. `t` (table | symbol | hsym | (hsym; symbol; symbol)):  Table or table reference.


**Returns** (table):  Metadata of the table.

## .qx.tbl.foreignKeys


Get foreign keys of a table. It's similar to [fkeys](https://code.kx.com/q/ref/fkeys/) but supports table name besides value.
For partitioned table, the latest partition is used. Note that this is supported only for the current database.

**Parameter:**

1. `t` (table | symbol):  Table or table name.


**Returns** (dict):  A dictionary that maps foreign-key columns to their tables.

## .qx.tbl.create


Create a new table with given data.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `data` (table):  Table data.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.

## .qx.tbl._addTable


Add an on-disk table.

**Parameter:**

1. `tablePath` (hsym):  Path to an on-disk table.
1. `data` (table):  Table data. Symbol columns must be enumerated and the table is not keyed.


**Returns** (hsym):  The path to the table.

## .qx.tbl.drop


Drop a table.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.

## .qx.tbl.describe


Describe a table reference.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.


**Returns** (dict(symbol -> symbol)):  A dictionary describing the table reference.

- `type` -> Table type, as returned by [.qx.tbl.getType](#qxtblgettype).
- `name` -> Table name.
- `dbDir` -> Database directory, or null if not applicable.
- `parField` -> Partition field, or null if not applicable.


**Throws:**

1. TypeError:  If `tabRef` is not of valid type.

## .qx.tbl.insert


Insert data into a table.
For partitioned tables, data need to be sorted by partitioned field.
Partial data are acceptable; the missing columns will be filled by type compliant nulls for simple columns
or empty lists for compound columns.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference
1. `data` (table):  Table data.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.

## .qx.tbl.update


Update values in certain columns of a table, similar to [functional update](https://code.kx.com/q/basics/funsql/#update)
but support all table types.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `criteria` (any[]):  A list of criteria where the select is applied to, or empty list for the whole table.
For partitioned tables, if partition field is included in the criteria, it has to be the first in the list.
1. `groupings` (dict | 0b):  A mapping of grouping columns, or `0b` for no grouping.
1. `columns` (dict):  Mappings from column names to columns/expressions.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.


**Throws:**

1. ColumnNotFoundError:  If a column from `columns` doesn't exist.

## .qx.tbl.selectLimit


Select from a table similar to [rank-5 functional select](https://code.kx.com/q/basics/funsql/#rank-5)
but support all table types.

**Parameter:**

1. `table` (table | symbol | hsym):  Table name, path or value.
1. `criteria` (any[]):  A list of criteria where the select is applied to, or empty list for the whole table.
1. `groupings` (dict | boolean):  A mapping of grouping columns, or `0b` for no grouping, `1b` for distinct.
1. `columns` (dict):  Mappings from column names to columns/expressions.
1. `limit` (int | long | (int;int) | (long;long)):  Limit on rows to return.


**Returns** (table):  Selected data from the table.

## .qx.tbl.selectLimitSort


Select from a table similar to [rank-6 functional select](https://code.kx.com/q/basics/funsql/#rank-6)
but support all table types.

**Parameter:**

1. `table` (table | symbol | hsym):  Table name, path or value.
1. `criteria` (any[]):  A list of criteria where the select is applied to, or empty list for the whole table.
1. `groupings` (dict | boolean):  A mapping of grouping columns, or `0b` for no grouping, `1b` for distinct.
1. `columns` (dict):  Mappings from column names to columns/expressions.
1. `limit` (int | long | (int;int) | (long;long)):  Limit on rows to return.
1. `sort` (any[]):  Sort the result by a column. The format is `(op;col)` where `op` is `>:` for descending and
  `<:` for ascending, and `col` is the column to be ordered by.


**Returns** (table):  Selected data from the table.

## .qx.tbl.deleteRows


Delete rows of a table given certain criteria.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `criteria` (any[]):  A list of criteria where matching rows will be deleted, or empty list to delete all rows.
For partitioned tables, if partition field is included in the criteria, it has to be the first in the list.


**Returns** (tabRef):  The table reference.

## .qx.tbl.raiseIfColumnNotFound


Raise ColumnNotFoundError if a column is not found from a table.

**Parameter:**

1. `table` (table | symbol | hsym | (hsym; symbol; symbol)):  Table value or reference.
1. `column` (symbol):  A column name.


**Throws:**

1. ColumnNotFoundError:  If the column doesn't exist.

## .qx.tbl.columnExists


Check if a column exists in a table.
For splayed tables, column existence requires that the column appears in `.d` file and its data file exists.
For partitioned tables, it requires the condition holds for the latest partition.

**Parameter:**

1. `table` (table | symbol | hsym | (hsym; symbol; symbol)):  Table value or reference.
1. `column` (symbol):  Column name.


**Returns** (boolean):  `1b` if the column exists in the table; `0b` otherwise.

## .qx.tbl.raiseIfColumnExists


Raise ColumnExistsError if a column exists in a table.

**Parameter:**

1. `table` (table | symbol | hsym | (hsym; symbol; symbol)):  Table value or reference.
1. `column` (symbol):  A column name.


**Throws:**

1. ColumnExistsError:  If the column exists.

## .qx.tbl.columns


Get column names of a table. It's similar to [cols](https://code.kx.com/q/ref/cols/#cols) but supports all table types.
For partitioned table, the latest partition is used.

**Parameter:**

1. `t` (table | symbol | hsym | (hsym; symbol; symbol)):  Table or table reference.


**Returns** (symbol[]):  Column names.

## .qx.tbl.addColumn


Add a column to a table with a given value.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `column` (symbol):  Name of new column to be added.
1. `columnValue` (any):  Value to be set on the new column.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.


**Throws:**

1. ColumnNameError:  If `column` is not a valid name.
1. ColumnExistsError:  If `column` already exists.

## .qx.tbl.raiseIfColumnNameInvalid


Raise ColumnNameError if a column name is not valid, i.e. it collides with q's reserved words and implicit column `i`.

**Parameter:**

1. `name` (symbol):  A column name.


**Throws:**

1. ColumnNameError:  If the column name is not valid.

## .qx.tbl.deleteColumn


Delete a column from a table.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `column` (symbol):  A column to be deleted.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.

## .qx.tbl.renameColumns


Rename column(s) from a table.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table name.
1. `nameDict` (dict):  A dictionary from existing name(s) to new name(s).


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.


**Throws:**

1. ColumnNameError:  If the column name is not valid.
1. ColumnNotFoundError:  If some column doesn't exist.

## .qx.tbl.reorderColumns


Reorder columns of a table.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `firstColumns` (symbol[]):  First columns after reordering.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.


**Throws:**

1. ColumnNotFoundError:  If some column in `firstColumns` doesn't exist.

## .qx.tbl.copyColumn


Copy an existing column of a table to a new column.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `sourceColumn` (symbol):  Source column to copy from.
1. `targetColumn` (symbol):  Target column to copy to.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.


**Throws:**

1. ColumnNotFoundError:  If `sourceColumn` doesn't exist.
1. ColumnExistsError:  If `targetColumn` exists.
1. ColumnNameError:  If name of `targetColumn` is not valid.

## .qx.tbl.apply


Apply a function to a column of a table.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `column` (symbol):  Column where the function will be applied.
1. `function` (fn(any[]) -> any[]):  Function to be applied.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.


**Throws:**

1. ColumnNotFoundError:  If `column` doesn't exist.

## .qx.tbl.castColumn


Cast the datatype of a column of a table.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `column` (symbol):  Column whose datatype will be casted.
1. `newType` (symbol | char):  Name or character code of the new data type.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.


**Throws:**

1. ColumnNotFoundError:  If `column` doesn't exist.

## .qx.tbl.setAttr


Set attributes to a table. It's an extended form of [Set Attribute](https://code.kx.com/q/ref/set-attribute/)
that is applicable to tables.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `attrs` (dict):  A mapping from column names to attributes.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  The table reference.


**Throws:**

1. ColumnNotFoundError:  If some columns in `attrs` don't exist.

## .qx.tbl.getAttr


Get attributes of a table. It's an extended from of [attr](https://code.kx.com/q/ref/attr/)
that is applicable to tables.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.


**Returns** (dict):  A mapping from columns names to attributes, where columns without attributes are not included.

## .qx.tbl.count


Count rows of a table.
It's similar to [count](https://code.kx.com/q/ref/count/#count) but supports all table types.

**Parameter:**

1. `table` (table | symbol | hsym | (hsym; symbol; symbol)):  Table value or reference.


**Returns** (long):  Row count of the table.

## .qx.tbl.exists


Check if a table of given name exists.
For splayed table not in the current database, it's deemed existent if the directory exists.
For partitioned table not in the current database, it's deemed existent if the directory exists in either the first
or the last partition.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.


**Returns** (boolean):  `1b` if the table exists; `0b` otherwise.

## .qx.tbl.at


Get entries at given indices of a table.
It's similar to [.Q.ind](https://code.kx.com/q/ref/dotq/#qind-partitioned-index) but has the following differences:
- if `indices` are empty, an empty table of conforming schema is returned rather than an empty list.
- if `indices` go out of bound, an empty table of conforming schema is returned rather than raising 'par error

**Parameter:**

1. `table` (symbol | hsym | table):  Table name, path or value.
1. `indices` (int[] | long[]):  Indices to select from.


**Returns** (table):  Table at the given indices.

## .qx.tbl.rename


Rename a table.

**Parameter:**

1. `tabRef` (symbol | hsym | (hsym; symbol; symbol)):  Table reference.
1. `newName` (symbol):  New name of the table.


**Returns** (symbol | hsym | (hsym; symbol; symbol)):  New table reference.


**Throws:**

1. NameError:  If the table name is not valid, i.e. it collides with q's reserved words
1. NameExistsError:  If the name is in use

## .qx.tbl.fix


Fix a partitioned table based on a good partition. Fixable issues include:

- add `.d` file if missing
- add missing columns to `.d` file
- add missing data files to disk filled by nulls for simple columns or empty lists for compound columns
- remove excessive columns from `.d` file but leave data files untouched
- put columns in the right order

**Parameter:**

1. `tabRef` (symbol | (hsym; symbol; symbol)):  Table reference.
1. `refPartition` (date | month | int):  A good partition to which the fixing refers.


**Returns** (symbol | (hsym; symbol; symbol)):  The table reference.


**Throws:**

1. NotAPartitionedTableError:  If the table is not a partitioned table.

## .qx.tbl.key


Return the key of a table if it's keyed table, or generic null otherwise.
It's an alias of [key](https://code.kx.com/q/ref/key/#keys-of-a-keyed-table).

**Parameter:**

1. `t` (table | symbol | hsym | (hsym; symbol; symbol)):  Table or table reference.


**Returns** (table | ::):  Key of the table.

## .qx.tbl.keepAttr


Wrap a function that modifies a table but keep the original attributes.

**Parameter:**

1. `func` (func):  A function that modifies a table.


**Returns** (func):  A wrapper function that keeps the original attributes.

## .qx.tbl.diff


Find differences between two tables. Note that row order matters for unkeyed tables.

**Parameter:**

1. `x` (table):  The first table referred to as `x`.
1. `y` (table):  The second table referred to as `y`.


**Returns** (dict):  Differences between `x` and `y`.

- `xcols` (symbol) -> (symbol[]) Columns of `x` that don't exist in `y`
- `ycols` (symbol) -> (symbol[]) Columns of `y` that don't exist in `x`
- `xkeys` (symbol) -> (long[] | table) Keys or indices of `x` that don't exist in `y`
- `ykeys` (symbol) -> (long[] | table) Keys or indices of `y` that don't exist in `x`
- `pairs` (symbol) -> (dict | table) Pairs of differences where each pair is named by field and `x` or `y`, concatenated by underscore
