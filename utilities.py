"""
Helper utilities
"""

import glob
import os
import openpyxl


# TODO probably want to make download dir a variable
filenames = glob.glob(r'C:\Users\cmill\Downloads\PerformanceResultsWeightlifting*.xlsx')


def file_rename(filenames, cycle):
    """
    Opens files and renames them based on content
    :return: 
    """
    for f in filenames:
        wb = openpyxl.load_workbook(f)
        sheet1 = wb.get_sheet_by_name("Sheet1")
        lift = sheet1["L2"].value
        wb.close()
        dst = cycle + '_' + lift + '.xlsx' # will likely need to prepend dir to keep from being moved to wd
        os.rename(f, dst)


file_rename(filenames, 'summer18cycle')
