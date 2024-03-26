
# .qx.import


Utilities for importing packages and modules.

## .qx.import.Package


Package info.

**Datatype:** table([name:symbol] path:symbol)

## .qx.import.Module


Module info.

**Datatype:** table([name:symbol] package:symbol; path:symbol)

## .qx.import.addPackage


Add a package specified by a name and a path.

**Parameter:**

1. `name` (symbol):  Package name.
1. `path` (string | hsym):  Path to the package.


**Returns** (boolean):  `1b` if the path is added; `0b` if the path already exists.


**Throws:**

1. DirectoryNotFoundError:  If the path doesn't exist.
1. NotADirectoryError:  If the path is not a directory.

## .qx.import.removePackage


Remove a package.

**Parameter:**

1. `name` (symbol):  Package name.


**Returns** (boolean):  `1b` if the package is unloaded; `0b` if the package wasn't loaded.

## .qx.import.listPackages


List all loaded packages.

**Returns** (table):  A table of loaded packages and their paths.

## .qx.import.clearPackages


Clear all loaded packages.
## .qx.import.loadModule


Load a module.

**Parameter:**

1. `name` (string | symbol):  Module name.
1. `package` (symbol):  Package where the module exists.


**Returns** (boolean):  `1b` if the module is loaded; `0b` if the module has already been loaded.


**Throws:**

1. PackageNotFoundError:  If the package is not found.
1. ModuleNotFoundError:  If the module is not found.
1. ModuleNameError:  If the module name is not valid.

## .qx.import.searchModule


Search a module from a package.

**Parameter:**

1. `name` (string | symbol):  Module name.
1. `package` (symbol):  Package where the module exists.


**Returns** (hsym):  A path to the found module.


**Throws:**

1. PackageNotFoundError:  If the package is not found.
1. ModuleNotFoundError:  If the module is not found.
1. ModuleNameError:  If the module name is not valid.

## .qx.import.unloadModule


Unload a module.

**Parameter:**

1. `name` (string | symbol):  Module name.


**Returns** (boolean):  `1b` if the module is unloaded; `0b` if the module wasn't loaded.

## .qx.import.reloadModule


Reload a module.

**Parameter:**

1. `name` (string | symbol):  Module name.


**Throws:**

1. ModuleNotFoundError:  If the module is not found.

## .qx.import.listModules


List all loaded modules.

**Returns** (table):  A table of loaded modules and their packages and paths.

## .qx.import.clearModules


Clear all loaded modules.