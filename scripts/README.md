# **ATTENTION!**
Google's INSTR is a little bit different than sqlite's INSTR.
Google need to delete 1, while sqlite don't need to do so
pay attention to the difference: 

`INSTR(uc_course_id, '_') - 1`
## Google's INSTR
```sql
WITH tmp AS (
  SELECT uc_course_id, cc_course_id, suc.name as uc_name, scc.name as cc_name
  FROM `courses.transferable_course` tc 
    JOIN `schools.school` suc ON suc.id = CAST(SUBSTR(uc_course_id, 0, INSTR(uc_course_id, '_') - 1) AS INTEGER)
    JOIN `schools.school` scc ON scc.id = CAST(SUBSTR(cc_course_id, 0, INSTR(cc_course_id, '_') - 1) AS INTEGER)
)
```

## Sqlite's INSTR
```sql
WITH tmp AS (
    SELECT uc_course_id, cc_course_id, suc.name as uc_name
    FROM transferable_course tc
    JOIN school suc ON suc.id = CAST(SUBSTR(uc_course_id, 0, INSTR(uc_course_id, '_')) AS INTEGER)
)
SELECT *
FROM tmp
```