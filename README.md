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


## wodify.py: Automation (above TODO)

Script used to navigate to wodify and generate performance reports. Will update to generate attendance report. More object oriented approach than attempted with [previous wodify project]( https://github.com/channiemills/Wodify).

#### TODO 
- Generate reports needed for attendance.py
- Handle file downloads 
- Script to manipulate downloads to find max performances by exercise
- Script to manipulate downloads to calculate percentages based on athlete max by exercise
- Replace sleep steps with a more robust wait method
- Wrap all in a Windows console or executable that users can access and interact with easily. 
