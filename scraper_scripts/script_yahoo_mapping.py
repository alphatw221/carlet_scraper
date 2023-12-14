from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time

from selenium.common.exceptions import TimeoutException
import selenium

import db
import re
import traceback

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

RETRIES = 100
WAIT = 3

def init_browser():

    options = webdriver.ChromeOptions()

    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})

    browser = webdriver.Chrome(options=options)

    # options.add_argument("no-sandbox")
    # options.add_argument("--disable-extensions")
    # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    browser.get("https://autos.yahoo.com.tw/new-cars/research")
    WebDriverWait(browser, WAIT).until(EC.presence_of_element_located((By.CLASS_NAME, 'research-main')))

    return browser


def get_make_links(browser:webdriver.Chrome):
    while True:
        try:
            make_links = browser.find_elements(By.XPATH,f".//div[@class='research-main']//div[@class='research-wrapper']//div[@class='list']//a")
            break
        except Exception as e:
            print(e)
    return make_links

def initModelBrowser(url, retries=RETRIES):
    try:
        print(url)
        options = webdriver.ChromeOptions()
        # options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
        
        model_browser = webdriver.Chrome(options=options)

        # options.add_argument("no-sandbox")
        # options.add_argument("--disable-extensions")
        # model_browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        model_browser.get(url)
        WebDriverWait(model_browser, WAIT).until(EC.presence_of_element_located((By.CLASS_NAME, 'main')))

        return model_browser
    except Exception as e:
        print(e)
        if retries>0:
            time.sleep(5)
            return initModelBrowser(url, retries=retries-1)
        else:
            raise Exception()

def scroll_all_page(browser:webdriver.Chrome):

    h = ''
    while h != browser.execute_script("return document.body.scrollHeight"):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        h = browser.execute_script("return document.body.scrollHeight")
        print(h)
        time.sleep(2)


def get_model_links(browser:webdriver.Chrome):


    while True:
        try:
            model_links = browser.find_elements(By.XPATH,f".//div[@class='main']//div[@class='make-main jq-make-wrapper']/div[@class!='nav-holder nav']/a[@class='gabtn']")
            break
        except Exception as e:
            print(e)
    return model_links





def initSubModelBrowser(url, retries=RETRIES):
    try:
        print(url)

        options = webdriver.ChromeOptions()
        options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
        sub_model_browser = webdriver.Chrome(options=options)

        # options.add_argument("no-sandbox")
        # options.add_argument("--disable-extensions")
        # sub_model_browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


        sub_model_browser.get(url)
        WebDriverWait(sub_model_browser, WAIT).until(EC.presence_of_element_located((By.CLASS_NAME, 'model-wrapper')))

        return sub_model_browser
    except Exception as e:
        print(e)
        if retries>0:
            time.sleep(5)
            return initSubModelBrowser(url, retries=retries-1)
        else:
            raise Exception()

def get_sub_model_links(browser:webdriver.Chrome):


    while True:
        try:
            # sub_model_links = browser.find_elements(By.XPATH,f".//div[@class='model-wrapper']/ul/li[@class='model-sub']/a[@class='gabtn']")
            sub_model_links = browser.find_elements(By.XPATH,f".//div[@class='model-wrapper']/ul//a[@class='gabtn']")

            break
        except Exception as e:
            print(e)
    return sub_model_links


def initVehicleBrowser(url, retries=RETRIES):
    try:

        print(url)

        options = webdriver.ChromeOptions()
        options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
        vehicle_browser = webdriver.Chrome(options=options)

        # options.add_argument("no-sandbox")
        # options.add_argument("--disable-extensions")
        # vehicle_browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)



        vehicle_browser.get(url)
        WebDriverWait(vehicle_browser, WAIT).until(EC.presence_of_element_located((By.CLASS_NAME, 'main')))

        return vehicle_browser

    except Exception as e:
        print(e)
        if retries>0:
            time.sleep(5)
            return initVehicleBrowser(url, retries=retries-1)
        else:
            raise Exception()
def main():
        
    
    target_makes = [
                'BMW 寶馬', 
                'Audi 奧迪', 
                'M-Benz 賓士', 
                'Porsche 保時捷'
            ]
    

    make_ids = {'BMW 寶馬':4, 'Audi 奧迪':2, 'M-Benz 賓士':23, 'Porsche 保時捷':30}
    chinese_pattern = re.compile(r'[\u4e00-\u9fa5]')

    hp_pattern = re.compile(r'\d+hp')
    

    
    with db.local_carlet.Session() as session:
        # vehicles= session.query(db.local_carlet.models.Vehicle).filter(db.local_carlet.models.Vehicle.make.in_(target_makes)).order_by(db.local_carlet.models.Vehicle.id.asc()).limit(50)
        vehicles= session.query(db.local_carlet.models.Vehicle).filter(db.local_carlet.models.Vehicle.make.in_(target_makes)).yield_per(100)

                              
    for vehicle in vehicles:
        try:

            make = vehicle.make
            model = vehicle.model
            sub_model = vehicle.sub_model
            sub_model = chinese_pattern.sub('', sub_model)


            output = vehicle.output
            matches = hp_pattern.findall(output)
            output = matches[0] if matches else ''

            _displacement:str = vehicle.displacement
            try:
                displacement = int(_displacement.replace('cc',''))
                displacement = round(displacement/1000,2)
                displacement = round(displacement,1)
            except :
                displacement = ''

            # displacement = str(round((displacement/1000),-2))

            make_id = make_ids.get(make)
            year = model[:4]
            trim_level = f'{displacement} {sub_model}' if displacement else sub_model

            with db.local_carlet.Session() as session:
                session.query(db.local_carlet.models.VehicleModel).filter_by(make_id=make_id, year=year, trim_level=trim_level).update({'output': output})
                session.commit()

            print('-------------Vehivle----------------')
            print(f'Make : {make}')
            print(f'Model : {model}')
            print(f'Submodel : {sub_model}')
            print(f'_Displacement : {_displacement}')
            print(f'Displacement : {displacement}')
            print(f'Output : {output}')
            print(f'Make ID : {make_id}')
            print(f'Year : {year}')
            print(f'Trim Level : {trim_level}')
            print('--------------------------------')




            pass
        except:
            print(traceback.format_exc())
            continue




if __name__ == "__main__":

    main()
