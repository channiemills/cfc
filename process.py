import pandas as pd
import os.path
import math

from exercises import exercises
from coaches import coaches
from utilities import clean_name

# for leaderboard, may add param for percentages
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
            print('File does not exist for {}.'.format(exercise))


def process_metcons(cycle):
    for exercise in exercises['metcon']:
        f = cycle + '_' + clean_name(exercise) + '.xlsx'
        if os.path.isfile(f):
            # read in metcon data
            source = pd.read_excel(f)

            # reduce to useful columns
            metcon = source[['Athlete', 'Result', 'Is As Prescribed', 'Is Rx Plus']]

            # Get rid of lowest scores for people that may have tested more than once and sort
            metcon['Result'] = pd.to_datetime(metcon['Result'], format='%M:%S').dt.time
            metcon = metcon.sort_values('Result', ascending=True) # because lower is better with time duh
            metcon['duplicated'] = metcon.duplicated('Athlete', keep='first')
            metcon = metcon[metcon['duplicated'] == False]


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

            for df in metcon_dfs:
                if len(df) > 0:
                    g = df.Gender.unique()[0]
                    r = 'rx' if df['Is As Prescribed'].unique()[0] == True else 'rxp'
                    df[['Athlete', 'Result']].to_csv('{}_{}_{}_{}.csv'.format(cycle, clean_name(exercise), g, r), index=False)


def process_weightsheet(cycle):
    for exercise in exercises['weightlifting']:
        f = cycle + '_' + 'weightsheets_' + clean_name(exercise) + '.xlsx'
        if os.path.isfile(f):
            # read in lift data, will need to loop through
            source = pd.read_excel(f)

            # reduce to useful cols
            lift = source[['Date', 'Athlete', 'Athlete Name', 'Result']]

            # split out rep scheme from weight
            lift['Scheme'], lift['Weight'] = lift['Result'].str.split(' @ ', 1).str

            # strip 'lbs' from weight column and change to int
            lift['Weight'] = lift['Weight'].map(lambda x: x.rstrip(' lbs'))
            lift['Weight'] = lift['Weight'].apply(pd.to_numeric)

            # pull out testing dates '07/30/2018', '08/12/2018'
            testing_ind = (lift['Date'] >= '07/30/2018') & (lift['Date'] <= '08/12/2018') # TODO - don't hardcode
            lift_testing = lift.loc[testing_ind]
            lift_sixmo = lift.loc[~testing_ind]

            # reduce to rows of 1 x 1 (1RM) for teseters
            lift_1r = lift_testing[lift_testing['Scheme'] == '1 x 1']

## stuff i will have to do for both dfs
            # Get rid of lowest scores for people that may have tested more than once and sort
            lift_1r = lift_1r.groupby('Athlete', group_keys=False).apply(lambda x: x.loc[x.Weight.idxmax()])
            lift_sixmo = lift_sixmo.groupby('Athlete', group_keys=False).apply(lambda x: x.loc[x.Weight.idxmax()])

            # combine dataframes where people in sixmo are not in lift_1r
            common = lift_1r.merge(lift_sixmo, on=['Athlete'])
            non_testers = lift_sixmo[(~lift_sixmo['Athlete'].isin(common['Athlete']))]

            # Combine again
            lift_all = pd.concat([lift_1r, non_testers])

            # need to make sure everyone that is active is there

            membership = pd.read_excel('AthletesAndMembershipDetails.xlsx') # assumes this is there >.<
            members = membership[['Athlete', 'Athlete Name']]

            joined = pd.merge(members, lift_all, how='left')

            roster = joined[~joined['Athlete Name'].isin(coaches)]

            # get rid of unnecessary cols
            roster['Athlete Name'] = roster['Athlete Name'].str.upper()
            roster_sort = roster.sort_values('Athlete Name')
            roster_final = roster_sort[['Athlete Name', 'Weight']]

            # add pcts
            pcts = [i / 100.0 for i in range(40, 105, 5)]

            roster_final = roster_final.fillna(0)

            for pct in pcts:
                roster_final[str(round(pct*100))+'%'] = roster_final['Weight'].apply(lambda x: math.ceil((x * pct)/5) * 5) #math.ceil((joined_all['Weight'] * pct)/5) * 5

            roster_final = roster_final.drop('Weight', axis=1)
            # add something special for if front squat, use back squat file and take 80 pct of it

            if clean_name(exercise) == 'BackSquat':
                frontsquat = roster_final.copy()
                for col in list(frontsquat):
                    if col != 'Athlete Name':
                        frontsquat[col] = frontsquat[col].apply(lambda x: math.ceil((x * 0.8)/5) * 5)

                frontsquat.to_csv('weightsheets\\{}_FrontSquat_percentsheet.csv'.format(cycle), index=False) #assumes weightsheet dir exists

            roster_final.to_csv('weightsheets\\{}_{}_percentsheet.csv'.format(cycle, clean_name(exercise)), index=False)

        else:
            print('File does not exist for {}.'.format(exercise))


#process_lifts('summer18cycle')

#process_metcons('summer18cycle')

process_weightsheet('summer18cycle')
