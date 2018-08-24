# cfc
Scripts to assist crossfit gym with tech needs. More object oriented approach than attempted with [previous wodify project]( https://github.com/channiemills/Wodify).

## attendance.py

Script used to generate list of Gold Start attendance athletes. 
Top athletes by attendance for a given weightlifting cycle, broken up by gender.

## wodify.py: Automation

Script used to navigate to wodify and generate performance reports.

#### TODO
- Replace sleep steps with a more robust wait method
- Write out sample executions. Consider workflow options

## utilities.py: File manipulation

Download management.

#### TODO
- Improve to specify download directory
- Specify subdirectory by cycle

## process.py: Data manipulation

 Data manipulation for leaderboards (metcon and weightlifting) as well as weightlifting percentages.

#### TODO
- add attendance as a function here
- Encapsulate code for simpler function definitions. Definitely can reduce duplicate code, particularly in weightsheets.
  - Gender stuff can be simplified to take one df and return male and female versions
- Wrap all in a Windows console or executable that users can access and interact with easily. 


### General TODO
- Add checks to confirm necessary reports exist before going on to later steps
- Directory clean up