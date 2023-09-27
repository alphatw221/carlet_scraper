from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from selenium.common.exceptions import TimeoutException
import selenium

browser = webdriver.Chrome()
browser.get("https://www.liqui-moly.com/en/")

try:
    delay = 10
    btn = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'CybotCookiebotDialogBodyButtonDecline')))
    if btn:
        btn.click()
except TimeoutException:
    print('No Accept Cookie Dialog')
    pass


# id="CybotCookiebotDialogBodyButtonDecline"
# CybotCookiebotDialog

time.sleep(5)   

# vehicle_type_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-select"))
# vehicle_type_select.select_by_visible_text('Cars')

vehicle_brand_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-brand"))
vehicle_brands = [op.text for op in vehicle_brand_select.options]
# print(vehicle_brands)

for vehicle_brand in vehicle_brands[1:]:
    # print(vehicle_brand)
    # vehicle_brand_select.select_by_visible_text(vehicle_brand)
    vehicle_brand_select.select_by_visible_text('BMW (USA)')
    time.sleep(5)   


    vehicle_model_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-model"))
    vehicle_models = [op.text for op in vehicle_model_select.options]
    # print(vehicle_models)
    for vehicle_model in vehicle_models[1:]:
        vehicle_model_select.select_by_visible_text(vehicle_model)
        time.sleep(5)


        vehicle_type_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-vehicle-type"))
        vehicle_types = [op.text for op in vehicle_type_select.options]

        # print(vehicle_types)

        for vehicle_type in vehicle_types[1:]:
            vehicle_type_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-vehicle-type"))
            vehicle_type_select.select_by_visible_text(vehicle_type)
            time.sleep(10)

            reco_accordion = browser.find_element(By.ID, "reco-accordion")
            titles = reco_accordion.find_elements(By.CLASS_NAME,'panel-title')
            # titles = reco_accordion.find_elements(By.XPATH,'/div[@class="panel panel-default"]/div[@class="panel-heading collapsed"]/h4[@class="panel-title"]/span')
            # print(titles)
            for title in titles:
                print(title.text)

            # headings = reco_accordion.find_elements(By.CSS_SELECTOR,'panel-heading')
            headings = reco_accordion.find_elements(By.XPATH,'.//div[@class="panel-heading collapsed"]')

            for heading in headings:
                try:
                    heading.click()
                    time.sleep(1)
                except Exception:
                    browser.execute_script("arguments[0].click();", heading)

                    continue
            time.sleep(30)
            
        break
    break
# print(vehicle_brand_options)
# driver.close()



def liqui_moly_scraper(browser:webdriver.Chrome, vehicle_brand, vehicle_model, vehicle_type):


    vehicle_brand_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-brand"))
    vehicle_brand_select.select_by_visible_text('BMW (USA)')
    time.sleep(5)   


    vehicle_model_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-model"))
    vehicle_model_select.select_by_visible_text(vehicle_model)
    time.sleep(5)


    vehicle_type_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-vehicle-type"))
    vehicle_type_select.select_by_visible_text(vehicle_type)
    time.sleep(10)

    reco_accordion = browser.find_element(By.ID, "reco-accordion")
    titles = reco_accordion.find_elements(By.CLASS_NAME,'panel-title')
    # titles = reco_accordion.find_elements(By.XPATH,'/div[@class="panel panel-default"]/div[@class="panel-heading collapsed"]/h4[@class="panel-title"]/span')
    # print(titles)
    for title in titles:
        print(title.text)

    # headings = reco_accordion.find_elements(By.CSS_SELECTOR,'panel-heading')
    headings = reco_accordion.find_elements(By.XPATH,'.//div[@class="panel-heading collapsed"]')

    for heading in headings:
        try:
            heading.click()
            time.sleep(1)
        except Exception:
            browser.execute_script("arguments[0].click();", heading)

            continue

