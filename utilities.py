"""
Helper utilities
"""

import glob
import os
import pathlib
import openpyxl


# TODO probably want to change download dir

download_dir = r'C:\Users\cmill\Downloads'
filenames = glob.glob(rf'{download_dir}\PerformanceResultsWeightlifting*.xlsx')
metcons = glob.glob(rf'{download_dir}\PerformanceResultsMetcon*.xlsx')

def setup_dirs(cycle):
    pathlib.Path(rf'{cycle}\{cycle}_results').mkdir(parents=True, exist_ok=True)
    pathlib.Path(rf'{cycle}\{cycle}_downloads').mkdir(parents=True, exist_ok=True) 


def file_rename(filenames, cycle):
    """
    Opens files and renames them based on content
    :return: 
    """
    for f in filenames:
        wb = openpyxl.load_workbook(f)
        sheet1 = wb.get_sheet_by_name("Sheet1")
        header = list(sheet1.rows)[0]
        comp = [col.column for col in header if col.value == 'Component'][0]
        liftname = sheet1[comp+'2'].value
        wb.close()
        dst = f'{cycle}\\{cycle}_downloads\\{cycle}_{clean_name(liftname)}.xlsx' # will likely need to prepend dir to keep from being moved to wd
        os.rename(f, dst)
        print(f'Moved {f} to {dst}')


def clean_name(liftname):
    f = liftname.rsplit(" (CrossFit Commitment)")[0]
    return ''.join(l for l in f if l.isalnum())


def helper_file_rename(cycle):
    """Rename helper files downloaded from wodify.
    """
    helpers = ['TotalAttendanceHistory.xlsx',
               'Users.xlsx', 'AthletesAndMembershipDetails.xlsx']
    for helper in helpers:
        src = rf'{download_dir}\{helper}'
        dst = f'{cycle}\\{cycle}_downloads\\{cycle}_{helper}'
        os.rename(src, dst)
        print(f'Moved {helper} to {os.getcwd()}')

def main():
    setup_dirs('testing')

    helper_file_rename('testing')

    file_rename(filenames, 'testing')

    file_rename(metcons, 'testing')


if __name__ == '__main__':
    main()
