"""
Elements you have to click on to get things to work in Wodify
"""

import time
from exercises import exercises

from selenium.webdriver.support.ui import Select

# TODO - customize download dir per: https://stackoverflow.com/questions/46937319/how-to-use-chrome-webdriver-in-selenium-to-download-files-in-python

REPORTS_URL = 'https://app.wodify.com/Reporting/PerformanceResultsReportsListEntry.aspx'

class Login:

    home = REPORTS_URL
    username_fieldname = 'WDS_wt1$block$wtContentForm$wtUserNameInput'
    password_fieldname = 'WDS_wt1$block$wtContentForm$wtPasswordInput'
    login_fieldname = 'WDS_wt1$block$wtContentForm$wtLoginButton'

    def login(self, browser, username, password):
        browser.get(self.home)
        username_field = browser.find_element_by_name(self.username_fieldname)
        password_field = browser.find_element_by_name(self.password_fieldname)
        username_field.send_keys(username)
        password_field.send_keys(password)
        browser.find_element_by_name(self.login_fieldname).click()
        time.sleep(5)


class Reports:

    metcons_id = 'WodifyAdminTheme_wt23_block_WodifyAdminThemeBase_wt16_block_wtMainContent_W_Widgets_UI_wt13_block_wtContent_wtMainContent_wtReportsTableRecords_ctl04_W_Widgets_UI_wt4_block_wtViewButtonPlaceholder_wt26'
    weightlifting_id = 'WodifyAdminTheme_wt23_block_WodifyAdminThemeBase_wt16_block_wtMainContent_W_Widgets_UI_wt13_block_wtContent_wtMainContent_wtReportsTableRecords_ctl08_W_Widgets_UI_wt4_block_wtViewButtonPlaceholder_wt26'
    # weightlifiting_href_xpath = '//a[@href="ReportRedirect.aspx?ReportId=11"]' 
    date_xpath = "//select[contains(@id, 'DateRange')]"
    date_from_xpath = "//input[contains(@id, 'DateInputFrom')]"
    date_to_xpath = "//input[contains(@id, 'DateInputTo')]"
    component_xpath = "//select[contains(@id, 'Component')]"
    export_xpath = "//a[contains(@id, 'Export')]"

    whitespace_id = "WodifyAdminTheme_wt14_block_WodifyAdminThemeBase_wt16_block_wtMainContent_W_Widgets_UI_wt13_block_wtContent"
    whitespace_id_metcon = "WodifyAdminTheme_wt51_block_WodifyAdminThemeBase_wt16_block_wtMainContent_W_Widgets_UI_wt13_block_wtContent"

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
            # browser.find_element_by_id(self.metcons_id).click()
            browser.find_element_by_xpath('//a[contains(@href, "ReportId=2")]').click()
        elif report_type == 'weightlifting':
            # browser.find_element_by_xpath(self.weightlifiting_href_xpath).click()
            # browser.find_element_by_id(self.weightlifting_id).click()
            browser.find_element_by_xpath('//a[contains(@href, "ReportId=11")]').click()
        else:
            print('Report type {} not implemented'.format(report_type))

        time.sleep(1.5)

    def pull_reports(self, browser, report_type, exercise, from_date, to_date): # won't need to pass in report type when validation put elsewhere
        """
        
        :param browser: 
        :param exercise: List of exercises to search
        :return: 
        """
        browser.get(REPORTS_URL)
        self.open_reports(browser, report_type)

        self.set_dates(browser, from_date, to_date) #consider making date class properties

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
                time.sleep(5)
                if report_type == 'metcon':
                    whitespace = browser.find_element_by_id(self.whitespace_id_metcon)
                else:
                    whitespace = browser.find_element_by_id(self.whitespace_id)

                whitespace.click()
                expt = browser.find_element_by_xpath(self.export_xpath)
                expt.click()
                time.sleep(5)

    def athlete_report(self, browser):
        """
        
        :param browser: 
        :return: Complete member roster at time of pull
        """
        athlete_report_id = "WodifyAdminTheme_wt2_block_WodifyAdminThemeBase_wt16_block_wtMainContent_W_Widgets_UI_wt13_block_wtContent_wtMainContent_wtReportsTableRecords_ctl02_W_Widgets_UI_wt21_block_wtViewButtonPlaceholder_wt12"
        athlete_report_href_xpath = '//a[@href="ReportRedirect.aspx?ReportId=19"]'
        program_xpath = "//select[contains(@id, 'Programs')]"
        browser.find_element_by_link_text("ATHLETES").click()
        # browser.find_element_by_id(athlete_report_id).click()
        browser.find_element_by_xpath(athlete_report_href_xpath).click()
        program = Select(browser.find_element_by_xpath(program_xpath))
        program.select_by_visible_text('CrossFit')
        time.sleep(2)
        expt = browser.find_element_by_xpath(self.export_xpath)
        expt.click()
        time.sleep(1)

    def attendance_report(self, browser, from_date, to_date):
        """
        
        :param browser: 
        :param from_date: 
        :param to_date: 
        :return: Total attendance for active members 
        """
        browser.get(REPORTS_URL)
        browser.find_element_by_class_name("menu-head_mobile-nav").click()
        browser.find_element_by_link_text("ATTENDANCE").click()
        total_attendance_href_xpath = '//a[@href="ReportRedirect.aspx?ReportId=29"]'
        browser.find_element_by_xpath(total_attendance_href_xpath).click()

        self.set_dates(browser, from_date, to_date)

        browser.find_element_by_class_name("Panel_content").click()
        time.sleep(10) # need to figure out how to wait for this to get everyone >.< 
        expt = browser.find_element_by_xpath(self.export_xpath)
        expt.click()
        time.sleep(1)

    def user_report(self, browser):
        checkbox_xpath = "//input[contains(@id, 'SelectAll')]"
        all_users_xpath = "//a[contains(@id, 'SelectAll')]"
        bulk_actions_id = "WodifyAdminTheme_wtLayout_List_WithFilterTabs_block_WodifyAdminThemeBase_wt17_block_wtMainContent_W_Widgets_UI_wt107_block_wtContent_TabFilters_UI_wtTabFilters_block_wtListOfRecords_W_Widgets_UI_wt106_block_wtText"

        browser.get(REPORTS_URL)
        browser.find_element_by_class_name("menu-head_mobile-nav").click()
        browser.find_element_by_link_text("PEOPLE").click()
        # browser.find_element_by_xpath('//a[@href="/AdminAthlete/UserListEntry.aspx"]').click()
        browser.find_element_by_link_text("ATHLETES").click()
        time.sleep(2)
        browser.find_element_by_xpath(checkbox_xpath).click()
        browser.find_element_by_xpath(all_users_xpath).click()
        time.sleep(1)
        browser.find_element_by_id(bulk_actions_id).click()
        browser.find_element_by_link_text("Export").click()
        time.sleep(1)

    def set_dates(self, browser, from_date, to_date):
        # Set custom date
        date = Select(browser.find_element_by_xpath(self.date_xpath))
        date.select_by_visible_text('Custom')
        time.sleep(2)
        # Set from and to dates
        date_from = browser.find_element_by_xpath(self.date_from_xpath)
        date_from.send_keys(from_date)
        date_to = browser.find_element_by_xpath(self.date_to_xpath)
        date_to.send_keys(to_date)
        time.sleep(2)
