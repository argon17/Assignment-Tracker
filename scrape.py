import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import creds


# for heroku
# import os

def login(driver):
    """
    login to teams using credentials provided
    """
    URL = 'https://teams.microsoft.com'
    driver.get(URL)
    time.sleep(10)
    emailFld = driver.find_element_by_id('i0116')
    print('logging in...')
    emailFld.click()
    emailFld.send_keys(creds.EMAIL)

    driver.find_element_by_id('idSIButton9').click()
    time.sleep(3)
    passwdFld = driver.find_element_by_id('i0118')
    passwdFld.click()
    passwdFld.send_keys(creds.PASSWD)

    driver.find_element_by_id('idSIButton9').click()
    time.sleep(3)
    driver.find_element_by_id('idBtn_Back').click()
    time.sleep(5)


def load_asgn(driver):
    """
    returns assignments description as a list
    """
    WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((By.ID, "app-bar-66aeee93-507d-479a-a3ef-8f494af43945")))
    asgnm = driver.find_element_by_xpath('//*[@id="app-bar-66aeee93-507d-479a-a3ef-8f494af43945"]')
    asgnm.click()
    time.sleep(5)

    try:
        data = []
        print(driver.title)
        print('switching to iframe...')
        driver.switch_to.frame('embedded-page-container')
        print('switched to iframe, finding assignments...')
        WebDriverWait(driver, 1000).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@data-e2e="assignment-card-description"]')))
        asgn = driver.find_elements_by_xpath('//*[@data-e2e="assignment-card-description"]')
        meta = driver.find_elements_by_xpath('//*[contains(@class,"assignment-card-duedate")]')
        print(f"{len(asgn)} assignments found...")
        for i, j in zip(asgn, meta):
            data.append([i.text, j.text])
        driver.switch_to.default_content()
        driver.quit()
        return data
    except:
        print("couldn't found")


def get_list(data):
    """
    removes useless characters and getting fresh list
    """
    course = [data[i][1].split('\n')[0] for i in range(len(data))]
    title = [data[i][0] for i in range(len(data))]
    due = [data[i][1].split('\n')[-1] for i in range(len(data))]
    lst = []
    for i, j, k in zip(course, title, due):
        k = k[:-6] + ',' + k[-6:]
        lst.append([i, j, k])

    return lst


def format_arr(lst):
    """
    formats the list to final text
    """
    for i in range(len(lst)):
        lst[i][0] = f"<b>{i + 1}. {lst[i][0]}</b>"

    t = ["\n".join(ele) for ele in lst]
    text = f"Hello Prem, there are {len(t)} assignments pending in Teams" \
           "\nMake sure you complete these on time:)\n\n" + "\n\n".join(t)
    return text


# for local machine

def get_assgnms():
    """
    initializes the driver and returns the final text to send
    """
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=creds.DRIVER_PATH,
                              chrome_options=chrome_options
                              )
    login(driver)
    data = load_asgn(driver)
    lst = get_list(data)
    return format_arr(lst)

# for heroku
# def get_assgnms():
#     chrome_options = Options()
#     chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument('--disable-dev-shm-usage')
#     chrome_options.add_argument('--no-sandbox')
#     driver = webdriver.Chrome(executable_path=os.environ.get("CHROME_DRIVER_PATH"),
#                               chrome_options=chrome_options
#                               )
#     login(driver)
#     data = load_asgn(driver)
#     lst = get_list(data)
#     return format_arr(lst)
