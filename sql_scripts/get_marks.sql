select student_lastname, student_name, student_patronymic, subject_name, mark
from marksview m
where student_lastname = '{}' and student_name = '{}' and student_patronymic = '{}'
order by mark_id asc