///
// Return the weekday after shifting a given number of weekdays from a given date. Note that the same date is
// returned when there is no shift.
// @param shift {long | int} Shift. A positive number shifts to the future, while a negative number shifts to the past.
// @return {date} The weekday after shifting `shift` weekdays from `d`.
// @throws {ValueError} If `t` is a symbol vector but not a valid partitioned table ID.
// @deprecated
// @example
// q).qx.sql.to_fsel "select c1,c2 by c3 from t where c4"
// "?[t;enlist `c4;(enlist`c3)!enlist`c3;(`c1`c2)!`c1`c2]"
.qx.date.shift_weekday:{[d;shift]
  weeks:shift div 5;
  r:shift mod 5;
  $[r>=0; r .qx.date.next_weekday/ d+weeks*7; neg[r] .qx.date.prev_weekday/ d+weeks*7]
 };

///
// Return the weekday after shifting a given number of weekdays from a given date. Note that the same date is
// returned when there is no shift.
// @param shift {long | int} Shift. A positive number shifts to the future, while a negative number shifts to the past.
// @return {date} The weekday after shifting `shift` weekdays from `d`.
// @throws {ValueError} If `t` is a symbol vector but not a valid partitioned table ID.
// @deprecated
// @example
// q).qx.sql.to_fsel "select c1,c2 by c3 from t where c4"
// "?[t;enlist `c4;(enlist`c3)!enlist`c3;(`c1`c2)!`c1`c2]"
.qx.date.shift_weekday:{[d;shift]
  weeks:shift div 5;
  r:shift mod 5;
  $[r>=0; r .qx.date.next_weekday/ d+weeks*7; neg[r] .qx.date.prev_weekday/ d+weeks*7]
 };
