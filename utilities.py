"""
Helper utilities
"""

import glob
import os
import pathlib
import openpyxl

from conf_vars import CYCLE, DOWNLOADS_DIR, RESULTS_DIR


# TODO probably want to change download dir

CHROME_DOWNLOADS = r'C:\Users\cmill\Downloads'
lifts = glob.glob(rf'{CHROME_DOWNLOADS}\PerformanceResultsWeightlifting*.xlsx')
metcons = glob.glob(rf'{CHROME_DOWNLOADS}\PerformanceResultsMetcon*.xlsx')

def setup_dirs():
    """Create directories for cycle downloads and results if DNE
    """
    pathlib.Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)
    pathlib.Path(DOWNLOADS_DIR).mkdir(parents=True, exist_ok=True) 


def file_rename(filenames, cycle):
    """Opens files and renames them based on content
    PARAMETERS
    ----------
    filenames : list
        Filenames matching specific format
    cycle : str
        Name of cycle, will be on filenames
    """
    for f in filenames:
        wb = openpyxl.load_workbook(f)
        sheet1 = wb.get_sheet_by_name("Sheet1")
        header = list(sheet1.rows)[0]
        comp = [col.column for col in header if col.value == 'Component'][0]
        liftname = sheet1[comp+'2'].value
        wb.close()
        if liftname:
            dst = f'{DOWNLOADS_DIR}\\{cycle}_{clean_name(liftname)}.xlsx'
            os.rename(f, dst)
            print(f'Moved {f} to {dst}')
        if not liftname:
            print(f'No data in this file.')


def clean_name(liftname):
    """Strips unnecessary text from exercise name
    PARAMETERS
    ----------
    liftname : str
        Name of lift including extra text
    RETURNS
    -------
    cleaned_name : str
        Name without unnecessary text and spaces
    """
    f = liftname.rsplit(" (CrossFit Commitment)")[0]
    return ''.join(l for l in f if l.isalnum())


def helper_file_rename(cycle):
    """Rename helper files downloaded from wodify
    and relocates them to directories created in setup_dirs.
    PARAMETERS
    ----------
    cycle : str
        Name of cycle, will be on filenames
    RETURNS
    -------
    """
    helpers = ['TotalAttendanceHistory.xlsx',
               'Users.xlsx', 'AthletesAndMembershipDetails.xlsx']
    for helper in helpers:
        src = rf'{CHROME_DOWNLOADS}\{helper}'
        dst = f'{DOWNLOADS_DIR}\\{cycle}_{helper}'
        if os.path.isfile(src):
            os.rename(src, dst)
            print(f'Moved {helper} to {DOWNLOADS_DIR}')
        else:
            print(f'No such file {helper} at {src}')


def main():
    """Main function. Runs all in this file.
    """
    setup_dirs()
    helper_file_rename(CYCLE)
    file_rename(lifts, CYCLE)
    file_rename(metcons, CYCLE)


if __name__ == '__main__':
    main()
