-- Generate the State table

drop table if exists patient_teleCC_state;

create table patient_teleCC_state as
select * 
from patient_teleCC
WHERE prediction_datetime = '2024-12-03 12:00:00';

-- Generate the History Table
--   1) Take the last 12 measurements from each patient from full table.
--   2) Take only patients that are in the state table (some may have been recently discarged)
drop table if exists patient_teleCC_history_tmp;
drop table if exists patient_teleCC_history;

create table patient_teleCC_history_tmp as
with q1 as (
select PatientID, station_number, prediction_datetime, septic_shock_score, respiratory_score,
row_number() over (partition by patientID, station_number order by prediction_datetime desc) as pred_order                               
from patient_teleCC as t1
where prediction_datetime <= '2024-12-03 12:00:00'
)
select PatientID, station_number, prediction_datetime, septic_shock_score, respiratory_score 
from q1
where pred_order <= 12
;

create table patient_teleCC_history as
select t1.* from 
patient_teleCC_history_tmp as t1 join patient_teleCC_state as t2
on t1.PatientID = t2.PatientID and t1.station_number = t2.station_number;

drop table patient_teleCC_history_tmp;