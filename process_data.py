import pandas as pd
from exercises import exercises
import os.path

# for leaderboard, may add param for percentages
# TODO - remove people that tested multiple times, take highest
# TODO - consider pulling last 6 months, then filtering to testing period for leaderboard then can use one pull

def process_lifts(cycle):
    for exercise in exercises['weightlifting']:
        f = exercise + '_' + cycle + '.xlsx'
        if os.path.isfile(f):
            # read in lift data, will need to loop through
            source = pd.read_excel(f)

            # reduce to useful cols
            lift = source[['Athlete', 'Athlete Name', 'Result']]

            # split out rep scheme from weight
            lift['Scheme'], lift['Weight'] = lift['Result'].str.split(' @ ', 1).str

            # reduce to rows of 1 x 1 (1RM)
            lift_1r = lift[lift['Scheme'] == '1 x 1']

            # strip 'lbs' from weight column and change to int
            lift_1r['Weight'] = lift_1r['Weight'].map(lambda x: x.rstrip(' lbs'))
            lift_1r['Weight'] = lift_1r['Weight'].apply(pd.to_numeric)

            # Get rid of lowest scores for people that may have tested more than once and sort
            lift_1r = lift_1r.groupby('Athlete', group_keys=False).apply(lambda x: x.loc[x.Weight.idxmax()])
            lift_1r_sort = lift_1r.sort_values('Weight', ascending=False)

            # read in gender data and apply
            users = pd.read_excel('users.xlsx') # TODO - don't assume this will be here?

            # Look up gender
            lift_1r_sort['Gender'] = lift_1r_sort['Athlete'].map(users.set_index('User')['Gender'])

            lift_1r_male = lift_1r_sort[lift_1r_sort['Gender'] == 'Male']
            lift_1r_female = lift_1r_sort[lift_1r_sort['Gender'] == 'Female']

            # Write out
            # Write output
            lift_1r_male[['Athlete Name', 'Weight']].to_csv('{}_{}_male.csv'.format(cycle, exercise), index=False)
            lift_1r_female[['Athlete Name', 'Weight']].to_csv('{}_{}_female.csv'.format(cycle, exercise), index=False)

        else:
            print('File does not exist for lift: {}.'.format(exercise))


process_lifts('summer18cycle')
