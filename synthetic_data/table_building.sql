create table patient_teleCC_state as
select * 
from patient_teleCC
WHERE prediction_datetime = '2024-12-03 12:00:00';

drop table if exists patient_teleCC_history_tmp;
drop table if exists patient_teleCC_history;

create table patient_teleCC_history_tmp as
select PatientID, Sta6a, prediction_datetime, septic_shock_score, respiratory_score                                
from patient_teleCC as t1
where prediction_datetime &lt;= '2024-12-03 12:00:00';

create table patient_teleCC_history as
select * from 
patient_teleCC_history_tmp as t1 join patient_teleCC_state as t2
on t1.PatientID = t2.PatientID and t1.Sta6a = t2.Sta6a;

drop table patient_teleCC_history_tmp;