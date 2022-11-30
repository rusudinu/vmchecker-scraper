import json

from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re

if __name__ == '__main__':
    scrape_run = 0
    auth_username = ''
    auth_password = ''
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)
        auth_username = credentials['username']
        auth_password = credentials['password']

    login_url = 'https://vmchecker.cs.pub.ro/ui/'
    url = 'https://vmchecker.cs.pub.ro/ui/#ADC'
    driver = webdriver.Chrome(service=Service())
    driver.get(url)
    time.sleep(1)

    username = driver.find_elements(By.TAG_NAME, "input")[0]
    username.send_keys(auth_username)
    password = driver.find_elements(By.TAG_NAME, "input")[1]
    password.send_keys(auth_password)
    driver.find_element(By.TAG_NAME, 'button').click()

    time.sleep(2)

    while True:
        driver.get(url)
        time.sleep(1)
        table = driver.find_elements(By.CLASS_NAME, "Gi7xsw1ND")
        names_html = driver.find_elements(By.CLASS_NAME, "Gi7xsw1KD")
        table_rows = [names_html[i].text for i in range(len(names_html))]

        names = table_rows[2::2]
        status = table_rows[3::2]
        submission_time = []
        total_score = []

        for i in range(len(names)):
            row = table[i]
            row.click()
            time.sleep(0.2)

            pres = driver.find_elements(By.TAG_NAME, "pre")
            submission_time.append(pres[1].text[24:43])
            if status[i] == 'ok':
                score_row = re.findall(r'Total score on tests: \d+\.?\d+', driver.page_source)[0]
                total_score.append(score_row[22:26])
            else:
                total_score.append('0')

            print(submission_time)
            print(total_score)
            driver.find_element(By.XPATH, "//*[contains(text(), 'close')]").click()

        df = pd.DataFrame({'Name': names
                              , 'Status': status
                              , 'Submission time': submission_time
                              , 'Total score': total_score})
        df.to_csv(f'logs/data_{scrape_run}.csv', index=False)

        scrape_run += 1

        time.sleep(50)
