
# .qx.db


Utilities around database management.

## .qx.db.loadSym


Load sym file in a database directory while keeping a backup of the original one in memory.

**Parameter:**

1. `dbDir` (hsym):  A database directory.
1. `sym` (symbol):  Name of sym file.


**Returns** (symbol):  The name of sym file.


**Throws:**

1. FileNotFoundError:  If the sym file doesn't exist.

## .qx.db.recoverSym


Recover in-memory backup sym data.

**Parameter:**

1. `sym` (symbol):  Name of sym data.


**Returns** (symbol):  The name of sym file if it's recovered successfully; null symbol otherwise, e.g. if there is no backup of such name.

## .qx.db.load


Load database in a given directory.

**Parameter:**

1. `dir` (string | hsym):  Directory.


**See also:**

[.qx.db.reload](#qxdbreload)

## .qx.db.reload


Reload current database.

**See also:**

[.qx.db.load](#qxdbload)
