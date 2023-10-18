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


def init_browser():

    options = webdriver.ChromeOptions()

    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})

    browser = webdriver.Chrome(options=options)

    browser.get("https://autofiles.com/gas-tank-size/")
   
    time.sleep(10)
    return browser





def get_make_links(browser:webdriver.Chrome):
    while True:
        try:
            make_links = browser.find_elements(By.XPATH,f".//section[@class='all-makes']//a")
            break
        except Exception as e:
            print(e)
    return make_links

def initMakeBrowser(url):
    while True:
        try:
            
            options = webdriver.ChromeOptions()
            options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
            make_browser = webdriver.Chrome(options=options)
            make_browser.get(url)
            WebDriverWait(make_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'make__vehicle')))
            break
        except Exception as e:
            print(e)
            make_browser.quit()

    return make_browser

def get_model_links(browser:webdriver.Chrome):
    while True:
        try:
            model_links = browser.find_elements(By.XPATH,".//ul[@class='make__vehicle']//h3//a")
            break
        except Exception as e:
            print(e)
    return model_links

def initModelBrowser(url):
    while True:
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
            model_browser = webdriver.Chrome(options=options)
            model_browser.get(url)
            WebDriverWait(model_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'make__vehicle')))
            break
        except Exception as e:
            print(e)
            model_browser.quit()

    return model_browser

def main():

    while True:
        try:

            browser = init_browser()

            make_links = get_make_links(browser)

            makes = [{'name':make_link.text, 'url': make_link.get_attribute('href')} for make_link in make_links]

            # makes = [
            #     {'name': 'Acura', 'url': 'https://autofiles.com/gas-tank-size/acura/'}, 
            #     {'name': 'Aston Martin', 'url': 'https://autofiles.com/gas-tank-size/aston-martin/'}, 
            #     {'name': 'Audi', 'url': 'https://autofiles.com/gas-tank-size/audi/'}, 
            #     {'name': 'Bentley', 'url': 'https://autofiles.com/gas-tank-size/bentley/'}, 
            #     {'name': 'BMW', 'url': 'https://autofiles.com/gas-tank-size/bmw/'}, 
            #     {'name': 'Buick', 'url': 'https://autofiles.com/gas-tank-size/buick/'}, 
            #     {'name': 'Cadillac', 'url': 'https://autofiles.com/gas-tank-size/cadillac/'}, 
            #     {'name': 'Chevrolet', 'url': 'https://autofiles.com/gas-tank-size/chevrolet/'}, 
            #     {'name': 'Chrysler', 'url': 'https://autofiles.com/gas-tank-size/chrysler/'}, 
            #     {'name': 'Dodge', 'url': 'https://autofiles.com/gas-tank-size/dodge/'}, 
            #     {'name': 'Ferrari', 'url': 'https://autofiles.com/gas-tank-size/ferrari/'}, 
            #     {'name': 'FIAT', 'url': 'https://autofiles.com/gas-tank-size/fiat/'}, 
            #     {'name': 'Ford', 'url': 'https://autofiles.com/gas-tank-size/ford/'}, 
            #     {'name': 'Genesis', 'url': 'https://autofiles.com/gas-tank-size/genesis/'}, 
            #     {'name': 'GMC', 'url': 'https://autofiles.com/gas-tank-size/gmc/'}, 
            #     {'name': 'Honda', 'url': 'https://autofiles.com/gas-tank-size/honda/'}, 
            #     {'name': 'Hyundai', 'url': 'https://autofiles.com/gas-tank-size/hyundai/'}, 
            #     {'name': 'Infiniti', 'url': 'https://autofiles.com/gas-tank-size/infiniti/'}, 
            #     {'name': 'Jaguar', 'url': 'https://autofiles.com/gas-tank-size/jaguar/'}, 
            #     {'name': 'Jeep', 'url': 'https://autofiles.com/gas-tank-size/jeep/'}, 
            #     {'name': 'Kia', 'url': 'https://autofiles.com/gas-tank-size/kia/'}, 
            #     {'name': 'Lamborghini', 'url': 'https://autofiles.com/gas-tank-size/lamborghini/'}, 
            #     {'name': 'Land Rover', 'url': 'https://autofiles.com/gas-tank-size/land-rover/'}, 
            #     {'name': 'Lexus', 'url': 'https://autofiles.com/gas-tank-size/lexus/'}, 
            #     {'name': 'Lincoln', 'url': 'https://autofiles.com/gas-tank-size/lincoln/'}, 
            #     {'name': 'Lotus', 'url': 'https://autofiles.com/gas-tank-size/lotus/'}, 
            #     {'name': 'Maserati', 'url': 'https://autofiles.com/gas-tank-size/maserati/'}, 
            #     {'name': 'Mazda', 'url': 'https://autofiles.com/gas-tank-size/mazda/'}, 
            #     {'name': 'McLaren', 'url': 'https://autofiles.com/gas-tank-size/mclaren/'}, 
            #     {'name': 'Mercedes-Benz', 'url': 'https://autofiles.com/gas-tank-size/mercedes-benz/'}, 
            #     {'name': 'MINI', 'url': 'https://autofiles.com/gas-tank-size/mini/'}, 
            #     {'name': 'Mitsubishi', 'url': 'https://autofiles.com/gas-tank-size/mitsubishi/'}, 
            #     {'name': 'Nissan', 'url': 'https://autofiles.com/gas-tank-size/nissan/'}, 
            #     {'name': 'Porsche', 'url': 'https://autofiles.com/gas-tank-size/porsche/'}, 
            #     {'name': 'RAM', 'url': 'https://autofiles.com/gas-tank-size/ram/'}, 
            #     {'name': 'Rolls-Royce', 'url': 'https://autofiles.com/gas-tank-size/rolls-royce/'}, 
            #     {'name': 'Scion', 'url': 'https://autofiles.com/gas-tank-size/scion/'}, 
            #     {'name': 'Smart', 'url': 'https://autofiles.com/gas-tank-size/smart/'}, 
            #     {'name': 'Subaru', 'url': 'https://autofiles.com/gas-tank-size/subaru/'}, 
            #     {'name': 'Suzuki', 'url': 'https://autofiles.com/gas-tank-size/suzuki/'}, 
            #     {'name': 'Toyota', 'url': 'https://autofiles.com/gas-tank-size/toyota/'}, 
            #     {'name': 'Volkswagen', 'url': 'https://autofiles.com/gas-tank-size/volkswagen/'}, 
            #     {'name': 'Volvo', 'url': 'https://autofiles.com/gas-tank-size/volvo/'}]



            for make in makes:
                make_name = make.get('name')
                url = make.get('url')

                make_browser = initMakeBrowser(url)
                model_links = get_model_links(make_browser)

                models = [{'name':model_link.text,'url':model_link.get_property('href')} for model_link in model_links]
                print(models)


                for model in models:

                    model_url = model.get('url')
                    model_borwser = initModelBrowser(model_url)
                    

                    li_elements = model_borwser.find_elements(By.XPATH, ".//ul[@class='make__vehicle']/li")
                    

                    for li_element in li_elements:
                        try:
                            span = li_element.find_element(By.XPATH, "./h3/span")

                            specs_li = li_element.find_elements(By.XPATH, "./ul[@class='make__vehicle-specs']//li")

                            specs_text = []
                            for spec in specs_li:
                                specs_text.append(spec.text)


                            make_name
                            model = span.text
                            specs = ','.join(specs_text)
                            print('-------Car-------')
                            print(make_name)
                            print(model)
                            print(specs)
                            print('--------------------')
                            


                            with db.autofiles.Session() as session:

                                car = session.query(db.autofiles.car.Car).filter_by(
                                    make=make_name, model=model).first()
                                if not car:
                                    car = db.autofiles.car.Car(make=make_name, model=model, specs=specs)
                                    session.add(car)
                                    session.commit()
                                else:
                                    car.specs = specs
                                    session.commit()

                        except Exception as e:
                            # print('err')
                            continue
                    
                    model_borwser.quit()
                
                make_browser.quit()
            
            browser.quit()
            break
                     
        except:
            print(traceback.format_exc())
            pass


def test():
    browser = init_browser()


            

    make_links = browser.find_elements(By.XPATH,f".//section[@class='all-makes']//a")

    makes = [{'name':make_link.text,'path':make_link.get_property('href')} for make_link in make_links]

    print(makes)
    while True:
        pass

if __name__ == "__main__":

    main()
    # test()