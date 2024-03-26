
# .qx.err


This contains predefined types of errors and functions to compose structured errors.

## .qx.err.Errors


A list of supported error types, including:

- `ColumnExistsError`: when a column of some name exists unexpectedly
- `ColumnNameError`: when a name for table column is not valid
- `ColumnNotFoundError`: when a column is requested but doesn't exist
- `DirectoryNotFoundError`: when a directory is requested but doesn't exist
- `FileNotFoundError`: when a file or directory is requested but doesn't exist
- `ModuleNameError`: when a module name is not valid
- `ModuleNotFoundError`: when a module cannot be found
- `NameError`: when a name collides with reserved names
- `NameExistsError`: when a name has already existed
- `NotADirectoryError`: when an operation for directory is requested on something not a directory
- `NotAPartitionedTableError`: when an operation for partitioned table is requested on something not a partitioned table
- `OSError`: when a system function returns a system-related error
- `PackageNotFoundError`: when a package is requested but doesn't exist
- `RuntimeError`: when an error is detected that doesn't fall in any of the other categories
- `ValueError`: when a variable has the right type but an inappropriate value
- `SchemaError`: when an operation operates on a table that has an inappropriate schema
- `TypeError`: when an inappropriate type is observed
- `UnknownErrorError`: when an error type is unknown

**Datatype:** symbol[]

## .qx.err.compose


Compose an error message via error type and description.

**Parameter:**

1. `err_type` (symbol):  Error type, which should be one of [.qx.err.Errors](#qxerrerrors).
1. `description` (string):  Error description.


**Returns** (string):  An error message of format "{errorType}: {msg}".


**Throws:**

1. UnknownErrorError:  If `errorType` is not supported.


**Example:**

```q
q)'.qx.err.compose[`TypeError; "expect int but got symbol"]
'TypeError: expect int but got symbol
  [0]  ' .qx.err.compose[`TypeError; "expect int but got symbol"]
         ^
```
