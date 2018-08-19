import pandas as pd
from exercises import exercises
import os.path
from utilities import clean_name

# for leaderboard, may add param for percentages
# TODO - remove people that tested multiple times, take highest
# TODO - consider pulling last 6 months, then filtering to testing period for leaderboard then can use one pull

def process_lifts(cycle):
    for exercise in exercises['weightlifting']:
        f = cycle + '_' + exercise + '.xlsx'
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

            # Write output
            lift_1r_male[['Athlete Name', 'Weight']].to_csv('{}_{}_male.csv'.format(cycle, exercise), index=False)
            lift_1r_female[['Athlete Name', 'Weight']].to_csv('{}_{}_female.csv'.format(cycle, exercise), index=False)

        else:
            print('File does not exist for lift: {}.'.format(exercise))


def process_metcons(cycle):
    for exercise in exercises['metcon']:
        f = cycle + '_' + clean_name(exercise) + '.xlsx'
        if os.path.isfile(f):
            # read in metcon data
            source = pd.read_excel(f)

            # reduce to useful columns
            metcon = source[['Athlete', 'Result', 'Is As Prescribed', 'Is Rx Plus']]
            metcon = metcon.sort_values('Result', ascending=False)

            # Read in gender data and apply
            users = pd.read_excel('users.xlsx')

            # Athlete name
            users['Athlete Name'] = users['First Name'] + ' ' + users['Last Name']

            # Look up gender
            metcon['Gender'] = metcon['Athlete'].map(users.set_index('Athlete Name')['Gender'])

            # Break out Rx and Rx+
            metcon_rx = metcon[metcon['Is As Prescribed'] == True]
            metcon_rxp = metcon[metcon['Is Rx Plus'] == True]

            # Split on gender
            metcon_rx_female = metcon_rx[metcon_rx['Gender'] == 'Female']
            metcon_rx_male = metcon_rx[metcon_rx['Gender'] == 'Male']
            metcon_rxp_female = metcon_rxp[metcon_rxp['Gender'] == 'Female']
            metcon_rxp_male = metcon_rxp[metcon_rxp['Gender'] == 'Male']

            # Write out

            metcon_dfs = [metcon_rx_female, metcon_rx_male, metcon_rxp_female, metcon_rxp_male]
            ### need something here for if no results

            for df in metcon_dfs:
                if len(df) > 0:
                    g = df.Gender.unique()[0]
                    r = 'rx' if df['Is As Prescribed'].unique()[0] == True else 'rxp'
                    df[['Athlete', 'Result']].to_csv('{}_{}_{}_{}'.format(cycle, clean_name(exercise)), g, r, index=False)

            # metcon_rx_female[['Athlete', 'Result']].to_csv('{}_{}_female_rx.csv'.format(cycle, clean_name(exercise)), index=False)
            # metcon_rx_male[['Athlete', 'Result']].to_csv('{}_{}_male_rx.csv'.format(cycle, clean_name(exercise)), index=False)
            #
            # metcon_rxp_female[['Athlete', 'Result']].to_csv('{}_{}_female_rxp.csv'.format(cycle, clean_name(exercise)), index=False)
            # metcon_rxp_male[['Athlete', 'Result']].to_csv('{}_{}_male_rxp.csv'.format(cycle, clean_name(exercise)), index=False)

#process_lifts('summer18cycle')

process_metcons('summer18cycle')
