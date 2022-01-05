select s.subject_name, sgc.group_name, et.exam_date, et.exam_time, c.classroom_name
from exam_timetable et
left join subject as s on et.subject_id = s.subject_id
left join study_groups_codes as sgc on et.study_group_id = sgc.group_id
left join classroom as c on et.classroom_id = c.classroom_id
where sgc.group_name='{}'