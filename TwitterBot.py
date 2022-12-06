from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time


def account_info():
    with open('account_info.txt', 'r') as f:
        info = f.read().split()
        email = info[0]
        password = info[1]

    return email, password




PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)

def twitter_func():
    email, password = account_info()
    try:
        home_page = "https://twitter.com"
        driver.get(home_page)
        time.sleep(5)
        driver.maximize_window()

        driver.find_element(By.XPATH, "//*[text()='Sign in']").click()
        time.sleep(5)

        driver.find_element(By.XPATH, "//input[@name='text']").click()
        driver.find_element(By.XPATH, "//input[@name='text']").send_keys(email)

        driver.find_element(By.XPATH, "//*[text()='Next']").click()
        time.sleep(5)

        driver.find_element(By.XPATH, "//input[@name='password']").click()

        driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)

        driver.find_element(By.XPATH, "//*[text()='Log in']").click()

        '''next_btn = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div[6]')
        next_btn.click()

        password = driver.find_element(By.XPATH, "//input[@autocomplete='Password Reveal password']")
        password.send_keys(password)

        login_btn = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div/main/div/div/div/div[2]/div[2]/div[2]/div/div/div[1]/div/div')
        login_btn.click()'''

    except Exception as e:
        print(e)



twitter_func()

'''
tweet = "Hello this is my twitter bot."
option = Options()
option.add_argument('start-maximized')
driver = Chrome(options=options)'''

