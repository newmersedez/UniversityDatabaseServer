select lt.lesson_day, lt.lesson_time, lt.lesson_type, s.subject_name
from lesson_timetable as lt
left join subject s on lt.subject_id = s.subject_id
where lt.lesson_day = '{}'
order by lesson_id