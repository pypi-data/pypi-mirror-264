
# .qx.utils


General utilities.

## .qx.utils.stringify


Convert an object to readable format.

**Parameter:**

1. `x` (any):  An object.


**Returns** (string):  A readable format of the object.


**Example:**

```q
q)1 .qx.utils.stringify `a`b!1 2;
a| 1
b| 2
q)1 .qx.utils.stringify ([]c1:1 2);
c1
--
1
2
```

## .qx.utils.nameExists


Check if a name is in use.
It's an alias of [key](https://code.kx.com/q/ref/key/#whether-a-name-is-defined).

**Parameter:**

1. `name` (symbol):  Variable name.


**Returns** (boolean):  `1b` if the name is in use; `0b` otherwise.

## .qx.utils.raiseIfNameExists


Raise NameExistsError if a name is in use.

**Parameter:**

1. `name` (symbol):  Variable name.


**Throws:**

1. NameExistsError:  If the name is in use.

## .qx.utils.vectorToIntByBase


Get integer representation of a vector by given base.
It's the reverse of [.qx.utils.intToVectorByBase](#qxutilsinttovectorbybase), and
It's an alias of [sv](https://code.kx.com/q/ref/sv/#base-to-integer).

**Parameter:**

1. `base` (short | int | long):  Base.
1. `vector` (byte[] | short[] | int[] | long[]):  Encoded vector.


**Returns** (long):  An integer by evaluating the vector to the base.

## .qx.utils.intToVectorByBase


Get vector representation of an integer by given base.
It's the reverse of [.qx.utils.vectorToIntByBase](#qxutilsvectortointbybase), and
It's an alias of [vs](https://code.kx.com/q/ref/vs/#base-x-representation).

**Parameter:**

1. `base` (short | int | long):  Base.
1. `int` (short | int | long):  An integer.


**Returns** (long[]):  Vector representation of the integer by the base.

## .qx.utils.vectorToIntByBases


Get integer representation of an vector by given bases.
It's the reverse of [.qx.utils.intToVectorByBases](#qxutilsinttovectorbybases), and
It's an alias of [sv](https://code.kx.com/q/ref/sv/#base-to-integer).

**Parameter:**

1. `bases` (short[] | int[] | long[]):  Bases.
1. `vector` (byte[] | short[] | int[] | long[]):  Encoded vector.


**Returns** (long):  Integer representation of the vector by the bases. The first of the bases is not used in the calculation,
as the coefficient for the last of the vector is always 1.

## .qx.utils.intToVectorByBases


Get vector representation of an integer by given bases.
It's the reverse of [.qx.utils.vectorToIntByBases](#qxutilsvectortointbybases), and
It's an alias of [vs](https://code.kx.com/q/ref/vs/#base-x-representation).

**Parameter:**

1. `bases` (short[] | int[] | long[]):  Bases.
1. `int` (short | int | long):  An integer.


**Returns** (long[]):  Vector representation of the integer by given bases.

## .qx.utils.toIntByBytes


Get short/int/long from its byte representation.
It's the reverse of [.qx.utils.toBytesByInt](#qxutilstobytesbyint), and
similar to [sv](https://code.kx.com/q/ref/sv/#bytes-to-integer) but leaves out the first argument.

**Parameter:**

1. `vector` (byte[]):  Length-2/4/8 byte vector.


**Returns** (short | int | long):  The corresponding integer represented by the byte array.

## .qx.utils.toBytesByInt


Get byte representation of a short/int/long.
It's the reverse of [.qx.utils.toIntByBytes](#qxutilstointbybytes) and
similar to [vs](https://code.kx.com/q/ref/vs/#byte-representation) but leaves out the first argument.

**Parameter:**

1. `int` (short | int | long):  A short/int/long integer.


**Returns** (byte[]):  Byte representation of the integer.

## .qx.utils.toIntByBools


Get byte/short/int/long from its bit (boolean) representation.
It's the reverse of [.qx.utils.toBoolsByInt](#qxutilstoboolsbyint) and
similar to [sv](https://code.kx.com/q/ref/sv/#bits-to-integer) but leaves out the first argument.

**Parameter:**

1. `vector` (boolean[]):  Length-8/16/32/64 boolean vector.


**Returns** (byte | short | int | long):  The corresponding byte or integer represented by the boolean array.

## .qx.utils.toBoolsByInt


Get bit (boolean) representation of a byte/short/int/long.
It's the reverse of [.qx.utils.toIntByBools](#qxutilstointbybools) and
similar to [vs](https://code.kx.com/q/ref/vs/#bit-representation) but leave out the first argument.

**Parameter:**

1. `int` (byte | short | int | long):  A byte or short/int/long integer.


**Returns** (boolean[]):  Bit representation of the byte or integer.
