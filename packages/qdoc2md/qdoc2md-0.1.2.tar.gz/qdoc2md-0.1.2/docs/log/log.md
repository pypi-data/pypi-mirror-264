
# .qx.log


Logging utilities.

## .qx.log.LEVELS


Logging levels, including:

  - `debug`
  - `info`
  - `warn`
  - `error`
  - `critical`

**Datatype:** symbol[]

## .qx.log.level


Lowest logging level at which messages are logged. Its value should be one of [.qx.log.LEVELS](#qxloglevels).
Default to `info`.

**Datatype:** symbol

## .qx.log.debug


Log a message at `debug` level.

**Parameter:**

1. `msg` (any):  A message.

## .qx.log.info


Log a message at `info` level.

**Parameter:**

1. `msg` (any):  A message.

## .qx.log.warn


Log a message at `warn` level.

**Parameter:**

1. `msg` (any):  A message.

## .qx.log.error


Log a message at `error` level.

**Parameter:**

1. `msg` (any):  A message.

## .qx.log.critical


Log a message at `critical` level.

**Parameter:**

1. `msg` (any):  A message.

## .qx.log.format


Format a message.

**Parameter:**

1. `msg` (any):  A message.


**Returns** (string):  A formatted message.

## .qx.log.prefix


Prefix pattern, a string that are composed of the following dynamic fields and any static text:

  - `%w`: current handle
  - `%u`: user of current handle
  - `%m`: used memory size in megabytes, rounded down to nearest integer
  - `%h`: heap memory size in megabytes, rounded down to nearest integer
  - `%p`: peak memory size in megabytes, rounded down to nearest integer
  - `%a`: mmap size in megabytes, rounded down to nearest integer
  - `%s`: number of symbols used
  - `%y`: size of symbols used in megabytes, rounded down to nearest integer

**Datatype:** string


**Example:**

```q
q).qx.log.prefix:"%m|%h|%p";
q).qx.log.info "test";
2024.02.03T04:38:45.362 INFO  0|67|67 test
```

## .qx.log.COLORS


Color-to-code mapping, where colors include `default`, `white`, the following, and their `bg_*` and `lbg_*` variants for
background and light background respectively:

  - `black`
  - `red`
  - `green`
  - `orange`
  - `blue`
  - `magenta`
  - `cyan`

**Datatype:** dict

## .qx.log.format_color


Format a message with a given color.

**Parameter:**

1. `color` (symbol):  A color from [.qx.log.COLORS](#qxlogcolors).
1. `msg` (any):  A message.

## .qx.log.redirect_out


Redirect output to a file.

**Parameter:**

1. `path` (hsym):  File path.

## .qx.log.reset_out


Reset output to stdout.
## .qx.log.redirect_err


Redirect error to a file.

**Parameter:**

1. `path` (hsym):  File path.

## .qx.log.reset_err


Reset error to stderr.