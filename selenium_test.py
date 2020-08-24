from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import requests

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("https://www.amazon.in")
    time.sleep(10)
    header_id = "//*[@id='nav-xshop']/"
    header = driver.find_elements(by=By.XPATH, value=header_id + "a")
    time.sleep(1)
    header_names = [i.get_attribute("text") for i in header]
    xpath = [header_id + 'a[{}]'.format(i) for i in range(1, len(header) + 1)]
    url = [i.get_attribute("href") for i in header]
    validation = []
    counter = 0
    for i in xpath:
        driver.find_element(by=By.XPATH, value=i).click()
        time.sleep(3)
        if driver.current_url == url[counter]:
            validation.append("Passed")
        else:
            validation.append("Failed")
        driver.back()
        time.sleep(3)
        counter += 1
    df = {'header_names': header_names, 'x_path': xpath, 'url': url, 'validation': validation}
    df = pd.DataFrame(df)
    excel = pd.ExcelWriter("output.xlsx")
    df.to_excel(excel)
    excel.save()
