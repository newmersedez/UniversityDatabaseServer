select student_lastname,student_name, student_patronymic, group_name,
study_degree_name, form_of_education_name, speciality_code, speciality_name
from AuthView
where
	student_login='{}' and student_password ='{}'