select lesson_day, lesson_time, lesson_type, classroom_name, subject_name
from lessons_view lv
where group_name='{}'
order by lesson_id