
# .qx.os


Operating system utilities.

## .qx.os.mkdir


Create a directory. The parent directory in the path will be created if it doesn't exist.

**Parameter:**

1. `path` (hsym):  Path to the directory.

## .qx.os.listdir


List files and directories under a path, in ascending order.
It's similar to [key](https://code.kx.com/q/ref/key/#files-in-a-folder) but raises errors if the directory doesn't exist
or the argument isn't a directory.

**Parameter:**

1. `path` (hsym):  Path to directory.


**Returns** (symbol[]):  Items under the directory in ascending order.


**Throws:**

1. FileNotFoundError:  If `path` doesn't exist.
1. NotADirectoryError:  If `path` is not a directory.

## .qx.os.copy


Copy a file from a source to a target.

**Parameter:**

1. `src` (hsym):  Source path.
1. `dst` (hsym):  Destination path.

## .qx.os.move


Move a file from source to destination.

**Parameter:**

1. `src` (hsym):  Source path.
1. `dst` (hsym):  Destination path.


**Throws:**

1. IsADirectoryError:  If `src` is a file and `dst` is a directory.
1. NotADirectoryError:  If `src` is a directory and `dst` is a file.

## .qx.os.remove


Remove a file.

**Parameter:**

1. `file` (hsym):  File path.

## .qx.os.rmtree


Remove a directory and all items under it.

**Parameter:**

1. `dir` (hsym):  Directory path.


**Throws:**

1. NotADirectoryError:  If `dir` is not a directory.
1. OSError:  If `dir` is a symlink to a directory.

## .qx.os.cleardir


Remove all under a directory.

**Parameter:**

1. `dir` (hsym):  Directory path.


**Throws:**

1. FileNotFoundError:  If `dir` doesn't exist.
1. NotADirectoryError:  If `dir` is not a directory.
