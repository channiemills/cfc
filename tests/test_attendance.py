"""
Tests for the attendance module
"""
import os
import shutil
from unittest import TestCase

import pandas as pd
from pandas.testing import assert_frame_equal

from reporting import attendance as att

def get_att_df():
    att_df = pd.DataFrame({
        'Athlete': [
            'Athlete One',
            'Athlete Two',
            'Athlete Three',
            'Athlete Four',
            'Athlete One',
            'Athlete One',
            'Athlete Two',
            'Athlete Four',
            'Athlete One'
        ],
        'User': [1, 2, 3, 4, 1, 1, 2, 4, 1],
        'Class Start Date Time': [
            '11/01/2019 5:00 AM',
            '11/01/2019 5:00 AM',
            '11/01/2019 5:00 AM',
            '11/01/2019 5:00 AM',
            '11/02/2019 7:00 AM',
            '11/02/2019 12:30 PM',
            '11/03/2019 5:00 AM',
            '11/03/2019 5:00 AM',
            '11/03/2019 5:00 AM',
        ]
    })
    return att_df
    
def get_user_df():
    user_df = pd.DataFrame({
        'User': [1, 2, 3, 4, 5],
        'Gender': ['Male', 'Female', 'Female', 'Male', 'Male']
    })
    return user_df


class TestAttendance(TestCase):
    """
    Tests for the attendance module.
    """

    def setUp(self):
        self.test_dir = 'temp_files'
        self.attendance_file = f'{self.test_dir}/attendance.txt'
        self.user_file = f'{self.test_dir}/users.txt'
        os.mkdir(self.test_dir)
        files = [self.attendance_file, self.user_file]

        for file_path in files:
            with open(file_path, 'w') as file_path:
                pass

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_helper_files_exist_true(self):
        assert att._helper_files_exist(self.attendance_file, self.user_file)

    def test_helper_files_exist_false(self):
        assert not att._helper_files_exist(self.attendance_file, 'foo.txt')
    
    def test_attendance_leaderboard(self):
        att_df = get_att_df()
        user_df = get_user_df()

        expected_att_male = pd.DataFrame({
            'User': [1, 4],
            'Athlete': ['Athlete One', 'Athlete Four'],
            'Count': [3, 2],
            'Gender': ['Male', 'Male']
        })

        expected_att_female = pd.DataFrame({
            'User': [2, 3],
            'Athlete': ['Athlete Two', 'Athlete Three'],
            'Count': [2, 1],
            'Gender': ['Female', 'Female']
        })

        att_male, att_female = att.attendance_leaderboard(att_df, user_df)

        assert_frame_equal(expected_att_female, att_female.reset_index(drop=True), check_like=True)
        assert_frame_equal(expected_att_male, att_male.reset_index(drop=True), check_like=True)
