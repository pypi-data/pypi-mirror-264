
# .qx.os.path


Common pathname manipulations.

## .qx.os.path.isfile


Check if the path points to a file.

**Parameter:**

1. `path` (hsym):  Path to file/directory.


**Returns** (boolean):  `1b` if the path points to a file; `0b` otherwise.

## .qx.os.path.isdir


Check if the path points to a directory.

**Parameter:**

1. `path` (hsym):  Path to file/directory.


**Returns** (boolean):  `1b` if `path` is an existing directory; `0b` otherwise.

## .qx.os.path.islink


Check if the path is a symlink.

**Parameter:**

1. `path` (hsym):  File path.


**Returns** (boolean):  `1b` if `path` is a symlink; `0b` otherwise.

## .qx.os.path.exists


Check if the path exists.

**Parameter:**

1. `path` (hsym):  Path to file/directory.


**Returns** (boolean):  `1b` if `path` refers to an existing path; `0b` otherwise.

## .qx.os.path.join


Join path segments. It's similar to [filepath-components overload of sv](https://code.kx.com/q/ref/sv/#filepath-components)
but moving the file handle out as a standalone argument.

**Parameter:**

1. `Path` (hsym):  Base path.
1. `segments` (symbol | symbol[]):  Path segments.


**Returns** (hsym):  A path by joining base path with the segments.

## .qx.os.path.split


Split a file path into directory and file parts. It's similar to [file handle overload of vs](https://code.kx.com/q/ref/vs/#file-handle)
but leaves out the first argument.

**Parameter:**

1. `path` (hsym):  A file path.


**Returns** (symbol[]):  Two-element symbol vector where the first is the directory part and the second the file part.

## .qx.os.path.string


Return path as a string.

**Parameter:**

1. `path` (symbol | hsym | string):  A file path, of either symbol, hsym, or string format.


**Returns** (string):  Path as a string.

## .qx.os.path.realpath


Get canonical path eliminating symlinks and up-level references.

**Parameter:**

1. `path` (hsym):  A file path.


**Returns** (hsym):  Canonical path eliminating symlinks and up-level references.

## .qx.os.path.samefile


Check if two paths point to the same file or directory.

**Parameter:**

1. `path1` (hsym):  A file path.
1. `path2` (hsym):  Another file path.


**Returns** (boolean):  `1b` if the two paths point to the same file or directory, `0b` otherwise.
