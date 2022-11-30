import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

if __name__ == '__main__':
    login_url = 'https://vmchecker.cs.pub.ro/ui/'
    url = 'https://vmchecker.cs.pub.ro/ui/#ADC'
    driver = webdriver.Chrome(service=Service())
    driver.get(url)
    time.sleep(1)

    username = driver.find_elements(By.TAG_NAME, "input")[0]
    username.send_keys('username')
    password = driver.find_elements(By.TAG_NAME, "input")[1]
    password.send_keys('password')
    driver.find_element('Login').click()

    time.sleep(1)

    driver.get(url)
    time.sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('tbody')
    print(table)
