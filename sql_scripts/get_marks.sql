select s.student_lastname, s.student_name, s.student_patronymic, s2.subject_name, m.mark
from marks as m
left join student s on m.student_id = s.student_id
left join subject s2 on m.subject_id = s2.subject_id
where s.student_lastname = '{}' and s.student_name = '{}' and s.student_patronymic = '{}'
order by mark_id asc