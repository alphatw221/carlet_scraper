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

# import concurrent.futures

import threading

browsers = []

def init_browser():
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
    browsers.append(browser)
    time.sleep(5)
    return browser


def init_browsers():

    threads = []
    for i in range(1):
        threads.append(threading.Thread(target = init_browser))
        threads[i].start()

    for i in range(1):
        threads[i].join()

    

def liqui_moly_scraper(browser:webdriver.Chrome, vehicle_make, vehicle_model:str, vehicle_sub_model:str):
    print('-------------------')
    print(vehicle_make, vehicle_model, vehicle_sub_model)
    print('-------------------')
    # browsers.append(browser)
    return
    try:

        # browser = webdriver.Chrome()
        # browser.get("https://www.liqui-moly.com/en/")
        # try:
        #     delay = 10
        #     btn = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'CybotCookiebotDialogBodyButtonDecline')))
        #     if btn:
        #         btn.click()
        # except TimeoutException:
        #     print('No Accept Cookie Dialog')
        #     pass
        print('-------------------')
        print(vehicle_make, vehicle_model, vehicle_sub_model)

        print('-------------------')

        vehicle_make_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-brand"))
        vehicle_make_select.select_by_visible_text(vehicle_make)
        time.sleep(15)   

        vehicle_model_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-model"))
        vehicle_model_select.select_by_visible_text(vehicle_model)
        time.sleep(15)

        vehicle_sub_model_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-vehicle-type"))
        vehicle_sub_model_select.select_by_visible_text(vehicle_sub_model)
        time.sleep(15)

        reco_accordion = browser.find_element(By.ID, "reco-accordion")
        titles = reco_accordion.find_elements(By.CLASS_NAME,'panel-title')
        # titles = reco_accordion.find_elements(By.XPATH,'/div[@class="panel panel-default"]/div[@class="panel-heading collapsed"]/h4[@class="panel-title"]/span')
        # print(titles)
        for title in titles:
            print(title.text)

        # headings = reco_accordion.find_elements(By.CSS_SELECTOR,'panel-heading')
        headings = reco_accordion.find_elements(By.XPATH,'.//div[@class="panel-heading collapsed"]')

        for heading in headings:
            browser.execute_script("arguments[0].click();", heading)
            time.sleep(1)
        # car_data = {}
        # year_pattern = r'\[[(\d{4}-\d{4}|\d{4}-)]\]'
        # engine_output_pattern = r'\((\d+ kW)\)'

        # matches = re.findall(year_pattern, vehicle_model)
        # start_year, end_year = None, None
        # for match in matches:
        #     year_range = match.split('-')

        #     start_year = year_range[0]
        #     end_year = year_range[1] if len(year_range) > 1 else ""

        #     vehicle_model = vehicle_model.replace(f'[{match}]', '')
        #     vehicle_model = vehicle_model.strip()

        #     vehicle_sub_model = vehicle_sub_model.replace(f'[{match}]', '')
        #     vehicle_sub_model = vehicle_sub_model.strip()

        # matches = re.findall(engine_output_pattern, vehicle_sub_model)
        # for match in matches:

        #     vehicle_sub_model = vehicle_sub_model.replace(f'({match})', '')
        #     vehicle_sub_model = vehicle_sub_model.strip()




        # with db.default.Session() as session:
        #     make = session.query(db.default.make.Make).filter_by(name=vehicle_make).first()
        #     if not make:
        #         make = db.default.make.Make(name='')
        #         session.add(make)
        #         session.commit()
            
        #     car = session.query(db.default.car.Car).filter_by(make=make, model=vehicle_model, sub_model=vehicle_sub_model)
        #     if not car:
        #         car = db.default.car.Car(make=make, model=vehicle_model, sub_model=vehicle_sub_model)
        #         session.add(car)
        #         session.commit()
    except Exception as e:
        print(vehicle_make, vehicle_model, vehicle_sub_model)
        print(e)
    browsers.append(browser)




def engine_processor(vehicle_brand, vehicle_model, vehicle_type, panel, car):
    try:
        title = panel.find_element(By.CLASS_NAME,'panel-title')

    except Exception:
        return



    if 'Engine' not in title.text:
         return
    

    pattern = r"Engine\s+[\w\s]+"

    matches = re.findall(pattern, title.text)
    engine_code = ['']
    for match in matches:
        match = match.replace('Engine','')
        engine_info = match.strip()
        engine_code.append(engine_info)
    engine_code = None if len(engine_code)==1 else ' '.join(engine_code)
    case_use, case_interval, case_capacity = '', '',''

    try:
        case_use = panel.find_element(By.XPATH,'.//div[@class="case use"]').text
    except Exception:
        pass
    try:
        case_interval = panel.find_element(By.XPATH,'.//div[@class="case interval"]').text
    except Exception:
        pass
    try:
        case_capacity = panel.find_element(By.XPATH,'.//div[@class="case capacity"]').text
    except Exception:
        pass

    print('-------Engine-------')
    print(engine_code)
    print(case_use)
    print(case_interval)
    print(case_capacity)
    print('--------------------')
    
    with db.liqui_moly.Session() as session:
        engine = session.query(db.liqui_moly.car.Engine).filter_by(car_id = car.id, code=engine_code).first()
        if not engine:
            engine = db.liqui_moly.car.Engine(car_id=car.id, code=engine_code, change_interval=f'{case_use}-{case_interval}', capacity=case_capacity)
            session.add(engine)
            session.commit()
        else:
            engine.change_interval = f'{case_use}-{case_interval}'
            engine.capacity = case_capacity
            session.commit()

    time.sleep(1)

def main():


    
    previous_make = 'BMW (EU)'
    previous_model = None
    previous_sub_model = None
    


    browser = init_browser()
 




    vehicle_brand_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-brand"))
    # vehicle_brands = [op.text for op in vehicle_brand_select.options]
    vehicle_brands = ['','BMW (EU)']

    for vehicle_brand in vehicle_brands[1:]:
        # print('.',vehicle_brand)
        vehicle_brand_select.select_by_visible_text(vehicle_brand)
        time.sleep(5)   

        vehicle_model_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-model"))
        vehicle_models = [op.text for op in vehicle_model_select.options]

        for vehicle_model in vehicle_models[1:]:
            # print('..',vehicle_model)
            vehicle_model_select.select_by_visible_text(vehicle_model)
            time.sleep(5)

            vehicle_type_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-vehicle-type"))
            vehicle_types = [op.text for op in vehicle_type_select.options]

            for vehicle_type in vehicle_types[1:]:

                vehicle_type_select = Select(browser.find_element(By.ID, "oww-vs-vehicle-vehicle-type"))
                vehicle_type_select.select_by_visible_text(vehicle_type)


                
                with db.liqui_moly.Session() as session:
                    session.expire_on_commit=False
                    
                    car = session.query(db.liqui_moly.car.Car).filter_by(
                        make=vehicle_brand, model=vehicle_model, sub_model=vehicle_type).first()
                    if not car:
                        car = db.liqui_moly.car.Car(make=vehicle_brand, model=vehicle_model, sub_model=vehicle_type)
                        session.add(car)
                        session.commit()

                    session.expunge(car)
                    db.liqui_moly.make_transient(car)

                time.sleep(15)

                reco_accordion = browser.find_element(By.ID, "reco-accordion")
                # titles = reco_accordion.find_elements(By.CLASS_NAME,'panel-title')

                # for title in titles:
                #     print(title.text)

                # # headings = reco_accordion.find_elements(By.CSS_SELECTOR,'panel-heading')
                # headings = reco_accordion.find_elements(By.XPATH,'.//div[@class="panel-heading collapsed"]')

                # for heading in headings:
                #     browser.execute_script("arguments[0].click();", heading)
                #     time.sleep(1)

                panels = reco_accordion.find_elements(By.XPATH,'./*')
                for panel in panels:


                    # try:
                    #     title = panel.find_element(By.CLASS_NAME,'panel-title')
                    #     print(title.text)
                    # except Exception:
                    #     continue

                    

                    # try:
                    #     heading = panel.find_element(By.XPATH,'.//div[@class="panel-heading collapsed"]')
                    #     browser.execute_script("arguments[0].click();", heading)
                    # except Exception:
                    #     pass
                    # time.sleep(1)

                    
                    engine_processor(vehicle_brand, vehicle_model, vehicle_type,panel, car)





if __name__ == "__main__":

    main()