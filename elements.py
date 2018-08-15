"""
Elements you have to click on to get things to work in Wodify
"""

import time
from exercises import exercises

from selenium.webdriver.support.ui import Select


class Login:

    home = 'https://app.wodify.com/Reporting/PerformanceResultsReportsListEntry.aspx'
    username_fieldname = 'wtLayoutLogin$SilkUIFramework_wt8$block$wtUsername$wtUsername$wtUserNameInput'
    password_fieldname = 'wtLayoutLogin$SilkUIFramework_wt8$block$wtPassword$wtPassword$wtPasswordInput'
    login_fieldname = 'wtLayoutLogin$SilkUIFramework_wt8$block$wtAction$wtAction$wtLoginButton'

    def login(self, browser, username, password):
        browser.get(self.home)
        username_field = browser.find_element_by_name(self.username_fieldname)
        password_field = browser.find_element_by_name(self.password_fieldname)
        username_field.send_keys(username)
        password_field.send_keys(password)
        browser.find_element_by_name(self.login_fieldname).click()
        time.sleep(3)


class Reports:

    metcons_id = 'WodifyAdminTheme_wt23_block_WodifyAdminThemeBase_wt16_block_wtMainContent_W_Widgets_UI_wt13_block_wtContent_wtMainContent_wtReportsTableRecords_ctl04_W_Widgets_UI_wt4_block_wtViewButtonPlaceholder_wt26'
    weightlifting_id = 'WodifyAdminTheme_wt23_block_WodifyAdminThemeBase_wt16_block_wtMainContent_W_Widgets_UI_wt13_block_wtContent_wtMainContent_wtReportsTableRecords_ctl08_W_Widgets_UI_wt4_block_wtViewButtonPlaceholder_wt26'
    date_xpath = "//select[contains(@id, 'DateRange')]"
    date_from_xpath = "//input[contains(@id, 'DateInputFrom')]"
    date_to_xpath = "//input[contains(@id, 'DateInputTo')]"
    component_xpath = "//select[contains(@id, 'Component')]"
    export_xpath = "//a[contains(@id, 'Export')]"

    def open_reports(self, browser, report_type):
        """
        Select from available reports in wodify. 
        :param report_type: 
        :return: 
        """
        if report_type not in [k for k in exercises.keys()]: # consider putting this at the start before login
            print('Report type not found')
            browser.quit()
        elif report_type == 'metcon':
            browser.find_element_by_id(self.metcons_id).click()
        elif report_type == 'weightlifting':
            browser.find_element_by_id(self.weightlifting_id).click()
        else:
            print('Report type {} not implemented'.format(report_type))

        time.sleep(1.5)

    def pull_reports(self, browser, report_type, exercise, from_date, to_date): # won't need to pass in report type when validation put elsewhere
        """
        
        :param browser: 
        :param exercise: List of exercises to search
        :return: 
        """
        # Set custom date
        date = Select(browser.find_element_by_xpath(self.date_xpath))
        date.select_by_visible_text('Custom')
        time.sleep(1)
        # Set from and to dates
        date_from = browser.find_element_by_xpath(self.date_from_xpath)
        date_from.send_keys(from_date)
        date_to = browser.find_element_by_xpath(self.date_to_xpath)
        date_to.send_keys(to_date)

        # Set component
        # validate component, consider putting this at the start, before logging in
        for exercise in exercise:
            if exercise not in exercises[report_type]:
                print('Invalid exercise: {}'.format(exercise))
                browser.quit()
            else:
                #component = Select(browser.find_element_by_id(self.component_id))
                component = Select(browser.find_elements_by_xpath(self.component_xpath)[1])
                component.select_by_visible_text(exercise)
                time.sleep(2)
                expt = browser.find_element_by_xpath(self.export_xpath)
                expt.click()
                time.sleep(1)
