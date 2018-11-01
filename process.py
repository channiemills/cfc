"""
Processes files downloaded from wodify and generate results.
"""

import os.path
import math
import pandas as pd

from exercises import exercises
from coaches import coaches
from utilities import clean_name

from conf_vars import CYCLE, DOWNLOADS_DIR, RESULTS_DIR, TESTING_START, TESTING_END


def lift_leaderboards(cycle, exercise, source):
    """Leaderboard for top lifters
    PARAMETERS
    ----------
    cycle : str
        Name of cycle, will prefix filename
    exercise : str
        Name of exercise, will be included in filename
    source : df
        Dataframe of performance during testing period
    RETURNS
    -------
    EXPORTS
    -------
    dataframes : csv
        Dataframe of Athlete and Weight for the exercise,
        sorted by top performance, one per gender.
    """
    # reduce to rows of 1 x 1 (1RM)
    lift_1r = source[source['Scheme'] == '1 x 1'][
                ~source['Athlete Name'].isin(coaches)]

    # Get rid of lowest scores for people that may have tested more than once and sort
    lift_1r = lift_1r.groupby('Athlete', group_keys=False).apply(lambda x: x.loc[x.Weight.idxmax()])
    lift_1r_sort = lift_1r.sort_values('Weight', ascending=False)

    users = pd.read_excel(f'{DOWNLOADS_DIR}\\{cycle}_Users.xlsx')
    lift_1r_sort['Gender'] = lift_1r_sort['Athlete'].map(users.set_index('User')['Gender'])
    lift_1r_male = lift_1r_sort[lift_1r_sort['Gender'] == 'Male']
    lift_1r_female = lift_1r_sort[lift_1r_sort['Gender'] == 'Female']

    lift_1r_male[['Athlete Name', 'Weight']].to_csv(
        f'{RESULTS_DIR}\\{cycle}_leaderboard_{exercise}_male.csv', index=False)
    lift_1r_female[['Athlete Name', 'Weight']].to_csv(
        f'{RESULTS_DIR}\\{cycle}_leaderboard_{exercise}_female.csv', index=False)


def metcon_leaderboards(cycle):
    """Leaderboard for top metcon athletes
    PARAMETERS
    ----------
    cycle : str
        Name of cycle, will prefix filename
    RETURNS
    -------
    EXPORTS
    -------
    dataframes : csv
        Dataframe of Athlete and performance for the metcon,
        sorted by top performance, one per gender per rx.
    """
    for exercise in exercises['metcon']:
        f = f'{DOWNLOADS_DIR}\\{cycle}_{clean_name(exercise)}.xlsx'
        if os.path.isfile(f):
            source = pd.read_excel(f)

            # reduce to useful columns
            metcon = source[['Athlete', 'Result', 'Is As Prescribed', 'Is Rx Plus']][
                ~source['Athlete'].isin(coaches)]

            # Get rid of lowest scores for people that may have tested more than once and sort
            if clean_name(exercise) == 'CFCCindy':
                metcon['Result'] = metcon['Result'].apply(lambda x: x.replace(' + ', '.'))
                metcon['Result'] = metcon['Result'].apply(pd.to_numeric)
                metcon = metcon.sort_values('Result', ascending=False)
                metcon['Result'] = metcon['Result'].astype(str)
                metcon['Result'] = metcon['Result'].apply(lambda x: x.replace('.', ' + '))
            else:
                metcon['Result'] = pd.to_datetime(metcon['Result'], format='%M:%S').dt.time
                metcon = metcon.sort_values('Result', ascending=True) # because lower is better with time duh

            metcon['duplicated'] = metcon.duplicated('Athlete', keep='first')
            metcon = metcon[~metcon['duplicated']]


            # Read in gender data and apply
            users = pd.read_excel(f'{DOWNLOADS_DIR}\\{cycle}_Users.xlsx')

            # Athlete name
            users['Athlete Name'] = users['First Name'] + ' ' + users['Last Name']

            # Look up gender
            metcon['Gender'] = metcon['Athlete'].map(users.set_index('Athlete Name')['Gender'])

            # Break out Rx and Rx+
            metcon_rx = metcon[metcon['Is As Prescribed']]
            metcon_rxp = metcon[metcon['Is Rx Plus']]

            # Split on gender
            metcon_rx_female = metcon_rx[metcon_rx['Gender'] == 'Female']
            metcon_rx_male = metcon_rx[metcon_rx['Gender'] == 'Male']
            metcon_rxp_female = metcon_rxp[metcon_rxp['Gender'] == 'Female']
            metcon_rxp_male = metcon_rxp[metcon_rxp['Gender'] == 'Male']

            # Write out

            metcon_dfs = [metcon_rx_female, metcon_rx_male, metcon_rxp_female, metcon_rxp_male]

            for df in metcon_dfs:
                if len(df) > 0:
                    gender = df.Gender.unique()[0]
                    rx = 'rx' if df['Is As Prescribed'].unique()[0] == True else 'rxp'
                    df[['Athlete', 'Result']].to_csv(
                        f'{RESULTS_DIR}\\{cycle}_leaderboard_{clean_name(exercise)}_{gender}_{rx}.csv', index=False)
            print(f'{exercise} results written to {RESULTS_DIR}')
        else:
            print(f'File does not exist for {exercise}.')


def weightsheets(cycle, start_date, end_date):
    """Weightsheets for all active members
    PARAMETERS
    ----------
    cycle : str
        Name of cycle, will prefix filename
    start_date : str
        Testing start date, used to filter for leaderboard
    end_date : df
        Testing end date, used to filter for leaderboard
    RETURNS
    -------
    EXPORTS
    -------
    dataframes : csv
        Dataframe of percentsheets for each exercise by athlete.
    """
    for exercise in exercises['weightlifting']:
        f = f'{DOWNLOADS_DIR}\\{cycle}_{clean_name(exercise)}.xlsx'
        if os.path.isfile(f):
            source = pd.read_excel(f)

            lift = source[['Date', 'Athlete', 'Athlete Name', 'Result']]

            lift['Scheme'], lift['Weight'] = lift['Result'].str.split(' @ ', 1).str

            lift['Weight'] = lift['Weight'].map(lambda x: x.rstrip(' lbs'))
            lift['Weight'] = lift['Weight'].apply(pd.to_numeric)

            testing_ind = (lift['Date'] >= start_date) & (lift['Date'] <= end_date)
            lift_testing = lift.loc[testing_ind]

            # get lift leaderboards
            lift_leaderboards(cycle, exercise, lift_testing)

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

            membership = pd.read_excel(f'{DOWNLOADS_DIR}\\{cycle}_AthletesAndMembershipDetails.xlsx') # assumes this is there >.<
            members = membership[['Athlete', 'Athlete Name']]
            members = members.drop_duplicates()

            joined = pd.merge(members, lift_all, how='left')

            joined = joined[['Athlete Name', 'Weight']][
                ~joined['Athlete Name'].isin(coaches)]
            
            joined['Athlete Name'] = joined['Athlete Name'].str.upper()

            joined_final = joined.sort_values('Athlete Name')

            low_pcts = [i / 100.0 for i in range(40, 70, 5)]
            high_pcts = [i / 1000.0 for i in range(675, 1025, 25)]
            pcts = low_pcts + high_pcts

            joined_final = joined_final.fillna(0)

            for pct in pcts:
                joined_final[str(round(pct*100, 1))+'%'] = joined_final['Weight'].apply(lambda x: math.ceil((x * pct)/5) * 5)

            joined_final = joined_final.drop('Weight', axis=1)

            if clean_name(exercise) == 'BackSquat':
                frontsquat = joined_final.copy()
                for col in list(frontsquat):
                    if col != 'Athlete Name':
                        frontsquat[col] = frontsquat[col].apply(lambda x: math.ceil((x * 0.8)/5) * 5)

                frontsquat.to_csv(
                    f'{RESULTS_DIR}\\{cycle}_percentsheet_FrontSquat.csv', index=False)

            joined_final.to_csv(
                f'{RESULTS_DIR}\\{cycle}_percentsheet_{clean_name(exercise)}.csv', index=False)
         
            print(f'{exercise} results written to {RESULTS_DIR}')

        else:
            print(f'File does not exist for {exercise}.')


def attendance_leaderboard(cycle):
    """Attendance leaderboard for cycle
    PARAMETERS
    ----------
    cycle : str
        Name of cycle, will be on filenames
    RETURNS
    -------
    EXPORTS
    -------
    dataframes : csv
        Attendance sorted by most, one for each gender
    """
    f = f'{DOWNLOADS_DIR}\\{cycle}_TotalAttendanceHistory.xlsx'
    u = f'{DOWNLOADS_DIR}\\{cycle}_Users.xlsx'
    if os.path.isfile(f) and os.path.isfile(u):
        users = pd.read_excel(u)
        att = pd.read_excel(f)

        # Group by user and sort based on attendance descending
        att_cycle_users = pd.DataFrame({'Count': att.groupby(['User', 'Athlete']).size()}).reset_index()
        att_sort = att_cycle_users.sort_values('Count', ascending=False)

        att_sort['Gender'] = att_sort['User'].map(users.set_index('User')['Gender'])
        att_male = att_sort[att_sort['Gender'] == 'Male']
        att_female = att_sort[att_sort['Gender'] == 'Female']

        att_male[['Athlete', 'Count']].to_csv(
            f'{RESULTS_DIR}\\{cycle}_attendance_male.csv', index=False)
        att_female[['Athlete', 'Count']].to_csv(
            f'{RESULTS_DIR}\\{cycle}_attendance_female.csv', index=False)

        print(f'Attendance results written to {RESULTS_DIR}')
    else:
        print(f'File does not exist for either {f} or {u}')


def main():
    """Main function. Calculates attendance, metcon and weight leaderboards,
    and weightshet percentages for current cycle.
    """
    # attendance_leaderboard(CYCLE)
    # metcon_leaderboards(CYCLE)
    weightsheets(CYCLE, TESTING_START, TESTING_END)


if __name__ == '__main__':
    main()
