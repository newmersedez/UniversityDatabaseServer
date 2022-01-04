select s.student_lastname, s.student_name, s.student_patronymic, sgc.group_name,
sd.study_degree_name, foe.form_of_education_name, s2.speciality_code, s2.speciality_name
from study_group sg
left join student s on sg.student_id =  s.student_id
left join study_groups_codes sgc on sg.study_group_code = sgc.group_id
left join speciality s2 on s.speciality_id = s2.speciality_id
left join study_degree sd on s.study_degree_id = sd.study_degree_id
left join form_of_education foe on s.form_of_education_id = foe.form_of_education_id
where
	s.student_login='{}' and s.student_password ='{}'