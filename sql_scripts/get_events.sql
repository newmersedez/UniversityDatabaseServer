select e.event_name, e.event_date, e.event_time, c.classroom_name, sgc.group_name
from events e
left join classroom c on e.classroom_id = c.classroom_id
left join study_groups_codes sgc on e.study_group_id = sgc.group_id