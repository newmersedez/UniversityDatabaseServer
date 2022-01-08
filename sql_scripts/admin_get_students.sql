select s.student_id, s.student_lastname, s.student_name, s.student_patronymic,
s.student_login, s.student_password
from student s
left join speciality s2 on s2.speciality_id = s.speciality_id
left join form_of_education foe ON foe.form_of_education_id = s.form_of_education_id
left join study_degree sd on sd.study_degree_id = s.study_degree_id
where s.student_name != 'admin'
order by s.student_id
