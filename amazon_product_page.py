from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("https://www.amazon.in")
    time.sleep(10)
    driver.find_element(by=By.ID, value='twotabsearchtextbox').send_keys(str(input('enter the product name : ')), Keys.RETURN)
    time.sleep(5)
    driver.find_element(by=By.XPATH, value="//div[@class='s-main-slot s-result-list s-search-results sg-row']//div[@data-cel-widget='search_result_1']//img").click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    links = driver.find_elements(by=By.XPATH, value="//*[@id='centerCol']//a[starts-with(@href, '/') and not(@target)]")
    link_names = [i.get_attribute('text') for i in links]
    xpath = ["//*[@id='centerCol']//a[text()='{}']".format(str(i)) for i in link_names]
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
    df = {'names': link_names , 'x_path': xpath, 'url': url, 'validation': validation}
    df = pd.DataFrame(df)
    excel = pd.ExcelWriter("product_page.xlsx")
    df.to_excel(excel)
    excel.save()
    driver.quit()