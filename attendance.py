"""
Script used to generate list of Gold Start attendance athletes. 
Top athletes by attendance for a given weightlifting cycle, broken up by gender.

Prerequisites: 
Pull total attendance from wodify.
Pull users from wodify.
- People > Athletes > Select all

Tech prerequisites:
Pandas

Coverage:
Look up athletes from attendance in users to get gender.
Export two csvs by gender, reporting attendance count for the period

# TODO - Using selenium or another tool, automatically download the needed reports (2) from Wodify
# TODO - Wrap in a Windows console or executable that users can access and interact with easily. 

"""

import pandas as pd
import os

# Read in data
users = pd.read_excel('users.xlsx')
att = pd.read_excel('TotalAttendanceHistory.xlsx')

# Receive cycle dates
start_date = input('Start date in YYYY-MM-DD format?')
end_date = input('End date in YYYY-MM-DD format?')

# Filter data based on cycle dates
att_cycle = att[(att['Class Start Date Time'] >= start_date) & (att['Class Start Date Time'] <= end_date)]

# Reduce to necessary columns
att_cycle_users = att_cycle[['User', 'Athlete']]

# Group by user and sort based on attendance descending
att_cycle_users = pd.DataFrame({'Count' : att_cycle.groupby( ['User', 'Athlete']).size()}).reset_index()
att_sort = att_cycle_users.sort_values('Count', ascending = False)

# Look up gender
att_sort['Gender'] = att_sort['User'].map(users.set_index('User')['Gender'])

att_male = att_sort[att_sort['Gender'] == 'Male']
att_female = att_sort[att_sort['Gender'] == 'Female']

# Write output
att_male[['Athlete', 'Count']].to_csv('male_attendance.csv', index=False)
att_female[['Athlete', 'Count']].to_csv('female_attendance.csv', index=False)

print('Results printed out to {}'.format(os.getcwd()))