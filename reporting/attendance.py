"""
Calculate the attendance leaderboard.
"""
import os

import pandas as pd


def _helper_files_exist(attendance_file_path, user_file_path) -> bool:
    return os.path.isfile(attendance_file_path) and os.path.isfile(user_file_path)


def _get_helper_dfs(attendance_file_path, user_file_path):
    """
    Reads in excel files
    """
    if not _helper_files_exist(attendance_file_path, user_file_path):
        raise ValueError('Missing attendance or user excel files')
    return pd.read_excel(attendance_file_path), pd.read_excel(user_file_path)


def attendance_leaderboard(attendance_df, users_df) -> tuple:
    """
    Calculates the attendance leaderboard

    Parameters
    ----------
    attendance_df : pandas.DataFrame()
        Dataframe of attendance data exported from Wodify
    users_df : pandas.DataFrame()
        Dataframe of user data exported from Wodify

    Returns
    -------
    tuple
        Tuple of two dateframes with attendance calculated and broken out by gender.
    """
    attendance_df['Class Start Date'] = pd.to_datetime(attendance_df['Class Start Date Time']).dt.date

    # Count unique days attended per user
    att_count = pd.DataFrame(
        {'Count': attendance_df.groupby(['User', 'Athlete'])
                  .apply(lambda x: len(x['Class Start Date'].unique()))
        }).reset_index()
    att_sort = att_count.sort_values('Count', ascending=False)

    # Add gender column
    att_sort['Gender'] = att_sort['User'].map(users_df.set_index('User')['Gender'])
    att_male = att_sort[att_sort['Gender'] == 'Male']
    att_female = att_sort[att_sort['Gender'] == 'Female']

    return att_male, att_female
