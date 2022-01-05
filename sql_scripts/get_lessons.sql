select lt.lesson_day, lt.lesson_time, lt.lesson_type, c.classroom_name, s.subject_name
from lesson_timetable as lt
left join subject s on lt.subject_id = s.subject_id
left join classroom c on lt.classroom_id = c.classroom_id
left join study_groups_codes sgc on lt.study_group_id = sgc.group_id
where sgc.group_name='{}'
order by lesson_id