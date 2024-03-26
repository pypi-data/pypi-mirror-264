
# .qx.date


Utilities around dates.

## .qx.date.day_of_week


Return the day of the week as an integer, where Monday is 1 and Sunday is 7.

**Parameter:**

1. `d` (date):  A date.


**Returns** (long):  The day of week as an integer, where Monday is 1 and Sunday is 7.

## .qx.date.is_weekday


Return `1b` if a date is a weekday; `0b` otherwise.

**Parameter:**

1. `d` (date):  A date.


**Returns** (boolean):  `1b` if `d` is a weekday; `0b` otherwise.

## .qx.date.next_weekday


Return the next weekday of a given date.

**Parameter:**

1. `d` (date):  A date.


**Returns** (date):  The next weekday of `d`.

## .qx.date.prev_weekday


Return the previous weekday of a given date.

**Parameter:**

1. `d` (date):  A date.


**Returns** (date):  The previous weekday of `d`.

## .qx.date.shift_weekday


Return the weekday after shifting a given number of weekdays from a given date. Note that the same date is
returned when there is no shift.

**Parameter:**

1. `d` (date):  A date.
1. `shift` (long | int):  Shift. A positive number shifts to the future, while a negative number shifts to the past.


**Returns** (date):  The weekday after shifting `shift` weekdays from `d`.

## .qx.date.weekdays_between


Return weekdays between two dates.

**Parameter:**

1. `d1` (date):  One date.
1. `d2` (date):  Another date.


**Returns** (date[]):  Weekdays between `d1` and `d2`.
