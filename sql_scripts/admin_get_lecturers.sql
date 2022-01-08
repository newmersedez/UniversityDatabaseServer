select l.lecturer_id, l.lecturer_lastname, l.lecturer_name, l.lecturer_patronymic, s.subject_name
from lecturer l
left join subject s on s.subject_id = l.subject_id
order by lecturer_id