from selenium import webdriver
from selenium.webdriver.support.ui import Select
from wodify_variables import username, password
import elements
from exercises import exercises
# from . import elements
# from . import exercises
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


browser = webdriver.Chrome()

wodify = elements.Login()
wodify.login(browser, username, password)

reports = elements.Reports()

# testing metcons

# reports.pull_reports(browser, 'metcon', exercises['metcon'], '10/08/2018', '10/21/2018')

# total attendance history
#reports.attendance_report(browser, '08/13/2018', '10/07/2018')

# athlete and member details
# reports.athlete_report(browser)

# users
# reports.user_report(browser)

# reports.pull_reports(browser, 'weightlifting', exercises['weightlifting'], '04/01/2018', '10/07/2018')

browser.quit()
