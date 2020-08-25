from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("https://www.amazon.in")
    time.sleep(10)
    header_id = "//*[@id='nav-xshop']/"
    header = driver.find_elements(by=By.XPATH, value=header_id + "a")
    footer = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[5]/div[1]/div').find_elements(by=By.TAG_NAME, value="a")
    time.sleep(1)
    header_names = [i.get_attribute("text") for i in header]
    footer_names = [i.get_attribute("text") for i in footer]
    xpath = ['//*[text()="{}"]'.format(str(i)) for i in (header_names + footer_names)]
    url = [driver.find_element(by=By.XPATH, value=i).get_attribute("href") for i in xpath]
    validation = []
    counter = 0
    for i in xpath:
        try:
            driver.find_element(by=By.XPATH, value=i).click()
        except Exception:
            validation.append("something went wrong")
        else:
            time.sleep(3)
            if driver.current_url == url[counter]:
                validation.append("Passed : directed to same url")
            else:
                validation.append("Failed : redirected to another url")
            driver.back()
        finally:
            time.sleep(3)
            counter += 1
    df = {'names': header_names + footer_names , 'x_path': xpath, 'url': url, 'validation': validation}
    df = pd.DataFrame(df)
    excel = pd.ExcelWriter("output.xlsx")
    df.to_excel(excel)
    excel.save()
    driver.close()
