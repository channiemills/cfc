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
#reports.open_reports(browser, 'metcon')

#reports.pull_reports(browser, 'metcon', 'CFC "Annie" (CrossFit Commitment)', '07/15/2018', '08/05/2018')


# testing lifts. will need to update ids on these

reports.open_reports(browser, 'weightlifting')

reports.pull_reports(browser, 'weightlifting', exercises['weightlifting'], '07/30/2018', '08/12/2018')

#import pdb; pdb.set_trace()
browser.quit()
