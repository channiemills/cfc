# cfc
Scripts to assist crossfit gym with tech needs. More object oriented approach than attempted with [previous wodify project]( https://github.com/channiemills/Wodify).

## wodify.py: Automation

Script used to navigate to wodify and generate performance reports.

#### TODO
- Replace sleep steps in elements.py with a more robust wait method
- Write out sample executions. Consider workflow options

## utilities.py: File manipulation

Download management.

#### TODO
- Improve to specify default download directory for chrome?

## process.py: Data manipulation

 Data manipulation for leaderboards (metcon and weightlifting) as well as weightlifting percentages.

#### TODO
- Encapsulate code for simpler function definitions. Definitely can reduce duplicate code, particularly in weightsheets.
  - Gender stuff can be simplified to take one df and return male and female versions
- Wrap all in a Windows console or executable that users can access and interact with easily. 


### General TODO
- Add checks to confirm necessary reports exist before going on to later steps
  -  before process.py
  - perhaps before utilities
- Current state, wodify.py gets all needed reports except user report. 
  - BUG : must update call for user report in wodify.py so that can be run standalone and in sequence with other reports

### Current Workflow
- Set cycle name and testing window in conf_vars.py
- Update wodify.py to reflect:
  - testing window
  - previous cycle dates (for attendance)
  - weightlifting history (testing_start - 6 months, testing_end)
  - TODO: move these into conf_vars
- Run wodify.py for everything but users
- Run wodify.py again for users (known bug)
- Run utilities.py
- Run process.py

### Dependencies
- Attendance:
  - Users.xlsx
  - TotalAttendanceHistory.xlsx

### Refactoring ideas
- Attendance
  - Raise error if missing files
  - UI Flow:
    - Click "Attendance"
    - Upload two files
    - Click "Submit"
      - Submit is probably an API endpoint that:
            - verifies the files exist
            - reads the two files into dataframes
            - calculates the attendance for m,f
            - returns csvs 
- General
  - Unit tests
    - continuous integration in gh + flake8
  - Docstrings
  - Update linter so all errors aren't treated as warnings
  - Helper function for splitting a df into two by gender
  - Consider putting in issues for these instead of tracking in readme