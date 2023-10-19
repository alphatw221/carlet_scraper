from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from selenium.common.exceptions import TimeoutException
import selenium

import db
import re
import traceback
from datetime import datetime

def init_browser():



    options = webdriver.ChromeOptions()

    # options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})

    # browser = webdriver.Chrome(options=options)
    # options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    # options.add_argument('--headless')
    # options.add_argument('--disable-javascript')

    browser = webdriver.Chrome(options=options)


    return browser



def getTireData(browser:webdriver.Chrome, car, make, model, year, additional):
    
    browser.get(f'https://www.tirerack.com/tires/SelectTireSize.jsp?autoMake={make}&autoModel={model}&autoYear={year}&autoModClar={additional}&perfCat=ALL')
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'optionWrapBtn')))

    try:
        options = browser.find_elements(By.XPATH,'.//li[@class="optionWrapBtn"]')
    except Exception:
        options = []


    for option in options:

        try:
            size_infos = option.find_elements(By.XPATH,'.//span[@class="sizeInfo"]')
        except Exception:
            print('get sizeInfo error')
            size_infos = []

        front_size = ''
        rear_size = ''
        size = ''
        
        for size_info in size_infos:
            
            try:
                label=size_info.find_element(By.XPATH,'./span[@class="tireSizeLabel"]').get_attribute("textContent")
            except Exception:
                label = ''
            
            try:
                width=size_info.find_element(By.XPATH,'./span[@class="sizeWidth"]').get_attribute("textContent")
            except Exception:
                width = 'na'

            try:
                detail=size_info.find_element(By.XPATH,'./span[@class="sizeLabel"]/span[@class="sizeDetail"]').get_attribute("textContent")
            except Exception:
                detail = 'na'

            try:
                msg=size_info.find_element(By.XPATH,'./span[@class="sizeLabel"]/span[@class="sizeMsg"]').get_attribute("textContent")
            except Exception:
                msg = 'na'
            

            if label=='Front Size':
                front_size = f'{width},{detail},{msg}'
            elif label=='Rear Size':
                rear_size = f'{width},{detail},{msg}'
            else:
                size = f'{width},{detail},{msg}'


        with db.tire_rack.Session() as session:

            tire_size = session.query(db.tire_rack.car.TireSize).filter_by(car_id=car.id, size=size, front_size=front_size, rear_size=rear_size, additional_info=additional).first()
            if not tire_size:
                tire_size = db.tire_rack.car.TireSize(car_id=car.id, size=size, front_size=front_size, rear_size=rear_size, additional_info=additional)
                session.add(tire_size)
                session.commit()


        print('-------------Tire----------------')
        print('Front Size:', front_size)
        print('Rear Size:', rear_size)
        print('Size:', size)
        print('---------------------------------')


def getWiperData(browser:webdriver.Chrome, car, make, model, year, additional):


    browser.get(f' https://www.tirerack.com/wipers/results.jsp?autoMake={make}&autoModel={model}&autoYear={year}&autoModClar={additional}')
    WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'productInfo')))
    
    try:
        product_specs = browser.find_elements(By.XPATH,'.//div[@class="productSpecs"]')
    except Exception:
        product_specs = []


    for product_spec in product_specs:

        try:
            manufacturer_part=product_spec.find_element(By.XPATH,'./ul').text
        except Exception:
            manufacturer_part = ''
        
        try:
            note=product_spec.find_element(By.XPATH,'./div[@class="noteText"]/span').get_attribute("textContent")
        except Exception:
            note = ''


        with db.tire_rack.Session() as session:

            wiper = session.query(db.tire_rack.car.Wiper).filter_by(car_id=car.id, manufacturer_part=manufacturer_part, note=note, additional_info=additional).first()
            if not wiper:
                wiper = db.tire_rack.car.Wiper(car_id=car.id, manufacturer_part=manufacturer_part, note=note, additional_info=additional)
                session.add(wiper)
                session.commit()


        print('-------------Wiper----------------')
        print('Manufacturer Part', manufacturer_part)
        print('Note:', note)
        print('---------------------------------')


def main():
    

    with db.tire_rack.Session() as session:
        cars= session.query(db.tire_rack.car.Car).filter_by(scraped_at=None).yield_per(100)

                              
    for car in cars:
        try:

            make = car.make
            model = car.model
            year = str(car.year)
            additional = car.sub_model

            print('-------------Car----------------')
            print(make)
            print(model)
            print(year)
            print(additional)
            print('--------------------------------')

            try:
                browser = init_browser()
                getTireData(browser, car, make, model, year, additional)
                browser.quit()
            except Exception:
                browser.quit()
                pass

            try:
                browser = init_browser()
                getWiperData(browser, car, make, model, year, additional)
                browser.quit()
            except Exception:
                browser.quit()
                pass

            with db.tire_rack.Session() as session:
                car= session.query(db.tire_rack.car.Car).filter_by(id=car.id).first()
                car.scraped_at = datetime.utcnow()
                session.commit()
            

        except Exception as e:
            browser.quit()
            print(e)
            continue


    #li optionWrapBtn

        # span sizeInfo
        #     span tireSizeLabel
        #     span sizeWidth
        #     span sizeLabel
        #         span sizeDetail
        #         span sizeMsg

        # span sizeInfo
        #     span tireSizeLabel  (Front Size, Rear Size)
        #     span sizeWidth
        #     span sizeLabel
        #         span sizeDetail
        #         span sizeMsg
    
 

    while True:
        pass
if __name__ == "__main__":

    main()
