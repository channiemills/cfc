# cfc
Scripts to assist crossfit gym with tech needs

## Attendance.py

Script used to generate list of Gold Start attendance athletes. 
Top athletes by attendance for a given weightlifting cycle, broken up by gender.

**Prerequisites:**

- Total attendance from wodify.
- Active users from wodify.
  - People > Athletes > Select all

**Tech prerequisites:**
- Pandas

**Coverage:**

- Look up athletes from attendance in users to get gender.
- Export two csvs by gender, reporting attendance count for the period

#### TODO - Using selenium or another tool, automatically download the needed reports (2) from Wodify
#### TODO - Wrap in a Windows console or executable that users can access and interact with easily. 