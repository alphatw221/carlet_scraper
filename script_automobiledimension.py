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
    browser.get("https://www.automobiledimension.com/")
   
    time.sleep(5)
    return browser





def get_make_links(browser:webdriver.Chrome):
    while True:
        try:
            make_links = browser.find_elements(By.XPATH,f".//div[@class='logos']/div/a")
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
            WebDriverWait(make_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'unit')))
            break
        except Exception as e:
            print(e)
            make_browser.quit()

    return make_browser

# def get_year_links(browser:webdriver.Chrome):
#     while True:
#         try:
#             year_panel = browser.find_element(By.XPATH,f".//div[@class='panel panel-default panel-linklist']")
#             year_links = year_panel.find_elements(By.XPATH,f".//div[@class='panel-body']/div[@class='list-group row']/a")
#             break
#         except Exception as e:
#             print(e)
#     return year_links

# def initYearBrowser(url):
#     while True:
#         try:
#             options = webdriver.ChromeOptions()
#             options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
#             yearl_browser = webdriver.Chrome(options=options)
#             yearl_browser.get(url)
#             WebDriverWait(yearl_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'panel-body')))
#             break
#         except Exception as e:
#             print(e)
#             yearl_browser.quit()

#     return yearl_browser

def get_models(browser:webdriver.Chrome):

    while True:
        try:
            models = []
            units = browser.find_elements(By.XPATH,f".//div[@class='unit']")

            for unit in units:
                try:
                    h2 = unit.find_element(By.XPATH,"./h2")
                    a = unit.find_element(By.XPATH,"./a")
                    url = a.get_attribute('href')
                    keys = url.split('/')

                    models.append({'name':h2.text, 'url':url, 'make_key':keys[-2], 'model_key':keys[-1]})
                except Exception as e:
                    print(e)
                    continue
            break
        except Exception as e:
            print(e)

    return models

def initModelBrowser(url):

    options = webdriver.ChromeOptions()
    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    model_browser = webdriver.Chrome(options=options)
    model_browser.get(url)
    WebDriverWait(model_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'interior-div')))


    return model_browser



def main():

    while True:
        try:

            previous_make_name,  previous_model_name = '',''

            with db.automobiledimension.Session() as session:
                previous_car = session.query(db.automobiledimension.car.Car).order_by(db.automobiledimension.car.Car.updated_at.desc()).first()
                if previous_car:
                    previous_make_name,  previous_model_name = previous_car.make_name, previous_car.model_name


            browser = init_browser()
            make_links = get_make_links(browser)

            makes = []
            for make_link in make_links:
                if previous_make_name:
                    if make_link.text == previous_make_name:
                        makes.append({'name':make_link.text, 'url': make_link.get_attribute('href')})
                        previous_make_name = ''
                    else:
                        continue
                else:
                    makes.append({'name':make_link.text, 'url': make_link.get_attribute('href')})

            for make in makes:
                
                make_name = make.get('name')
                url = make.get('url')

                make_browser = initMakeBrowser(url)
                
                models = get_models(make_browser)
                indicator = False
                for i in range(len(models)-1, -1, -1):
                    if indicator:
                        models.pop(i)
                    elif previous_model_name and previous_model_name == models[i].get('name'):
                        indicator = True

                for model in models:

                    try:

                        model_name = model.get('name')
                        model_url = model.get('url')
                        make_key = model.get('make_key')
                        model_key = model.get('model_key')

                        model_borwser = initModelBrowser(model_url)
                        
                        
                        for year in range(1990, 2024):
                            try:
                                img = model_borwser.find_element(By.XPATH,f".//img[@src='/photos/{make_key}-{model_key}-{year}.jpg']")

                                image_src = img.get_attribute('src')

                                with db.automobiledimension.Session() as session:

                                    car = session.query(db.automobiledimension.car.Car).filter_by(make=make_key, year = year, model=model_key).first()
                                    if not car:
                                        car = db.automobiledimension.car.Car(make=make_key, year = year, model=model_key, make_name=make_name, model_name=model_name, image_src=image_src)
                                        session.add(car)
                                        session.commit()
                                    else:
                                        car.image_src = image_src
                                        session.commit()



                                print('-------Car-------')
                                print(make_name)
                                print(make_key)
                                print(year)
                                print(model_name)
                                print(model_key)
                                print(image_src)
                                print('--------------------')



                            except Exception as e:
                                # print(f'{year}-not-found')
                                continue
                        


                        
                        model_borwser.quit()

                    except Exception as e:
                        continue

                make_browser.quit()
            
            browser.quit()
            break
                     
        except:
            print(traceback.format_exc())
            pass




if __name__ == "__main__":

    main()