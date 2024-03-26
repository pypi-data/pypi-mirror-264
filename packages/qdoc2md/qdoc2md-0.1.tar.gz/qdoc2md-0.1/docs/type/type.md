
# .qx.type


Type utilities.

## .qx.type.defaults


A mapping between type letters to their default values.

**Datatype:** dict(char->any)

## .qx.type.isTable


Check if an object is a table, simple or keyed.

**Parameter:**

1. `x` (any):  Any q object.


**Returns** (boolean):  `1b` if `x` represents a simple or keyed table; `0b` otherwise.

## .qx.type.ishsym


=Check if an object is an hsym.

**Parameter:**

1. `x` (any):  Any q object.


**Returns** (boolean):  `1b` if `x` is an hsym; `0b` otherwise.
