"""
Helper utilities
"""

import glob
import os
import openpyxl


# TODO probably want to make download dir a variable
filenames = glob.glob(r'C:\Users\cmill\Downloads\PerformanceResultsWeightlifting*.xlsx')
metcons = glob.glob(r'C:\Users\cmill\Downloads\PerformanceResultsMetcon*.xlsx')

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
        lift = clean_name(liftname)
        wb.close()
        dst = cycle + '_' + lift + '.xlsx' # will likely need to prepend dir to keep from being moved to wd
        os.rename(f, dst)


def clean_name(liftname):
    f = liftname.rsplit(" (CrossFit Commitment)")[0]
    return ''.join(l for l in f if l.isalnum())


file_rename(filenames, 'summer18cycle_weightsheets')

#file_rename(metcons, 'summer18cycle')
