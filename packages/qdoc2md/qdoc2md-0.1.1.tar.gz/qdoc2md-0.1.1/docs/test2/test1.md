
test1
=====

## .qx.date.shift_weekday


***Deprecated***


Return the weekday after shifting a given number of weekdays from a given date. Note that the same date is returned when there is no shift.

**Parameter:**

|Name|Type|Description|
| :--- | :--- | :--- |
|shift|long \| int| Shift. A positive number shifts to the future, while a negative number shifts to the past.|


**Returns:**

|Type|Description|
| :--- | :--- |
|date| The weekday after shifting `shift` weekdays from `d`.|


**Throws:**

|Type|Description|
| :--- | :--- |
|ValueError| If `t` is a symbol vector but not a valid partitioned table ID.|


**Example:**

```q
q).qx.sql.to_fsel "select c1,c2 by c3 from t where c4"
"?[t;enlist `c4;(enlist`c3)!enlist`c3;(`c1`c2)!`c1`c2]"
```

## .qx.date.shift_weekday


***Deprecated***


Return the weekday after shifting a given number of weekdays from a given date. Note that the same date is returned when there is no shift.

**Parameter:**

|Name|Type|Description|
| :--- | :--- | :--- |
|shift|long \| int| Shift. A positive number shifts to the future, while a negative number shifts to the past.|


**Returns:**

|Type|Description|
| :--- | :--- |
|date| The weekday after shifting `shift` weekdays from `d`.|


**Throws:**

|Type|Description|
| :--- | :--- |
|ValueError| If `t` is a symbol vector but not a valid partitioned table ID.|


**Example:**

```q
q).qx.sql.to_fsel "select c1,c2 by c3 from t where c4"
"?[t;enlist `c4;(enlist`c3)!enlist`c3;(`c1`c2)!`c1`c2]"
```
