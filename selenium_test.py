from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import requests
import openpyxl

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("https://www.amazon.in")
    time.sleep(10)
    header_id = "//*[@id='nav-xshop']/"
    header = driver.find_elements(by=By.XPATH, value=header_id + "a")
    time.sleep(1)
    header_names = [i.get_attribute for i in header]
    xpath = [header_id + 'a[{}]'.format(i) for i in range(1, len(header) + 1)]
    url = [i.get_attribute("href") for i in header]
    request = [requests.get(i).status_code for i in url]
    remarks = ['passed' if i == 200 else 'failed' for i in request]
    df = {'header_names': header_names, 'x_path': xpath, 'url': url, 'request': request, 'remarks': remarks}
    df = pd.DataFrame(df)
    excel = pd.ExcelWriter("output.xlsx")
    df.to_excel(excel)
    excel.save()