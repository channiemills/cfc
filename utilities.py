"""
Helper utilities
"""

import glob
import os
import openpyxl


# TODO probably want to make download dir a variable
filenames = glob.glob(r'C:\Users\cmill\Downloads\PerformanceResultsWeightlifting*.xlsx')
metcons = glob.glob(r'C:\Users\cmill\Downloads\PerformanceResultsMetcon*.xlsx')
attendance = glob.glob(r'C:\Users\cmill\Downloads\TotalAttendanceHistory.xlsx')
users = glob.glob(r'C:\Users\cmill\Downloads\Users.xlsx')

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
        dst = f'{cycle}_{clean_name(liftname)}.xlsx' # will likely need to prepend dir to keep from being moved to wd
        os.rename(f, dst)


def clean_name(liftname):
    f = liftname.rsplit(" (CrossFit Commitment)")[0]
    return ''.join(l for l in f if l.isalnum())


# file_rename(filenames, 'autumn18')

# file_rename(metcons, 'autumn18')
