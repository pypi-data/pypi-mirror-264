
# .qx.sql


Utilities for q-sql.

## .qx.sql.to_fsel


Return functional select form out of a q-sql query.

**Parameter:**

1. `query` (string):  A q-sql query.


**Returns** (string):  Functional select form of the query.


**Example:**

```q
q).qx.sql.to_fsel "select c1,c2 by c3 from t where c4"
"?[t;enlist `c4;(enlist`c3)!enlist`c3;(`c1`c2)!`c1`c2]"
```
