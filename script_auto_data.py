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

    # options.add_argument("no-sandbox")
    # options.add_argument("--disable-extensions")
    # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    browser.get("https://www.auto-data.net/en/allbrands")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'brands')))

    return browser





def get_make_links(browser:webdriver.Chrome):

    while True:
        try:
            make_links = browser.find_elements(By.XPATH,f".//div[@class='brands']//a[@class='marki_blok']")
            break
        except Exception as e:
            print(e)
    return make_links

def initModelCategoryBrowser(url):
    while True:
        try:
            
            options = webdriver.ChromeOptions()
            options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
            make_browser = webdriver.Chrome(options=options)

            # options.add_argument("no-sandbox")
            # options.add_argument("--disable-extensions")
            # make_browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


            make_browser.get(url)
            WebDriverWait(make_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'modelite')))
            break
        except Exception as e:
            print(e)
            make_browser.quit()

    return make_browser

def get_model_category_links(browser:webdriver.Chrome):

    while True:
        try:
            model_categories_link = browser.find_elements(By.XPATH,f".//ul[@class='modelite']//a[@class='modeli']")
            break
        except Exception as e:
            print(e)
    return model_categories_link


def get_model_links(browser:webdriver.Chrome):


    while True:
        try:
            model_links = browser.find_elements(By.XPATH,f".//table[@class='generr']//tr//th//a")
            break
        except Exception as e:
            print(e)
    return model_links

def initModelBrowser(url):

    options = webdriver.ChromeOptions()
    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    
    model_browser = webdriver.Chrome(options=options)

    # options.add_argument("no-sandbox")
    # options.add_argument("--disable-extensions")
    # model_browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    model_browser.get(url)
    WebDriverWait(model_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'generr')))

    return model_browser



def initSubModelBrowser(url):

    options = webdriver.ChromeOptions()
    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    sub_model_browser = webdriver.Chrome(options=options)

    # options.add_argument("no-sandbox")
    # options.add_argument("--disable-extensions")
    # sub_model_browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    sub_model_browser.get(url)
    WebDriverWait(sub_model_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'carlist')))

    return sub_model_browser


def get_sub_model_links(browser:webdriver.Chrome):


    while True:
        try:
            sub_model_links = browser.find_elements(By.XPATH,f".//table[@class='carlist']//tr//th//a")
            break
        except Exception as e:
            print(e)
    return sub_model_links

def initVehicleBrowser(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    vehicle_browser = webdriver.Chrome(options=options)

    # options.add_argument("no-sandbox")
    # options.add_argument("--disable-extensions")
    # vehicle_browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)



    vehicle_browser.get(url)
    WebDriverWait(vehicle_browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

    return vehicle_browser

def main():

    while True:
        try:

            previous_make, previous_model_category, previous_model, previous_sub_model = '','','',''

            with db.auto_data.Session() as session:
                previous_car = session.query(db.auto_data.car.Car).order_by(db.auto_data.car.Car.created_at.desc()).first()
                if previous_car:
                    previous_make, previous_model_category, previous_model, previous_sub_model = previous_car.make, previous_car.model_category, previous_car.model, previous_car.sub_model

            print(previous_make)
            print(previous_model_category)

            print(previous_model)

            print(previous_sub_model)

            browser = init_browser()
            make_links = get_make_links(browser)

            makes = []
            for make_link in make_links:
                if previous_make:
                    if make_link.text == previous_make:
                        makes.append({'name':make_link.text, 'url': make_link.get_attribute('href')})
                        previous_make = ''
                    else:
                        continue
                else:
                    makes.append({'name':make_link.text, 'url': make_link.get_attribute('href')})

            for make in makes:
                make_name = make.get('name')
                url = make.get('url')

                model_category_browser = initModelCategoryBrowser(url)
                model_category_links = get_model_category_links(model_category_browser)

                model_categories = []
                for model_category_link in model_category_links:
                    if previous_model_category:
                        if model_category_link.text == previous_model_category:
                            model_categories.append({'name':model_category_link.text,'url':model_category_link.get_property('href')})
                            previous_model_category = ''
                        else:
                            continue
                    else:
                        model_categories.append({'name':model_category_link.text,'url':model_category_link.get_property('href')})


                for model_category in model_categories:
                    model_category_name = model_category.get('name')
                    url = model_category.get('url')

                    model_browser = initModelBrowser(url)
                    model_links = get_model_links(model_browser)

                    models = []
                    for model_link in model_links:
                        if previous_model:
                            if model_link.text == previous_model:
                                models.append({'name':model_link.text, 'url': model_link.get_attribute('href')})
                                previous_model = ''
                            else:
                                continue
                        else:
                            models.append({'name':model_link.text,'url':model_link.get_property('href')})

                    for model in models:

                        model_name = model.get('name')
                        model_url = model.get('url')

                        sub_model_borwser = initSubModelBrowser(model_url)
                        sub_model_links = get_sub_model_links(sub_model_borwser)

                        sub_models = []
                        
                        for sub_model_link in sub_model_links:

                            if previous_sub_model:
                                if sub_model_link.text == previous_sub_model:
                                    sub_models.append({'name':sub_model_link.text, 'url': sub_model_link.get_attribute('href')})
                                    previous_sub_model = ''
                                else:
                                    continue
                            else:
                                sub_models.append({'name':sub_model_link.text,'url':sub_model_link.get_property('href')})

                        for sub_model in sub_models:
                            try:
                                sub_model_name = sub_model.get('name')
                                sub_model_link = sub_model.get('url')

                                vehicle_browser = initVehicleBrowser((sub_model_link))

                                trs = vehicle_browser.find_elements(By.XPATH,f".//table[@class='cardetailsout car2']//tr")



                                with db.auto_data.Session() as session:
                                    session.expire_on_commit=False
                            

                                    car = session.query(db.auto_data.car.Car).filter_by(make=make_name, model_category=model_category_name, model=model_name, sub_model=sub_model_name).first()
                                    if not car:
                                        car = db.auto_data.car.Car(make=make_name, model_category=model_category_name, model=model_name, sub_model=sub_model_name)
                                        session.add(car)
                                        session.commit()

                                    session.expunge(car)
                                    db.auto_data.make_transient(car)

                                print('-------------------------vehicle----------------')
                                print(f'Make : {make_name}')
                                print(f'Model Category : {model_category_name}')
                                print(f'Model : {model_name}')
                                print(f'Sub Model : {sub_model_name}')
                                print('------------------------------------------------')
                                print('-------------------------properties-------------')
                                for tr in trs:
                                    try:
                                        property_name = tr.find_element(By.XPATH,f"./th").text
                                        property_value = tr.find_element(By.XPATH,f"./td").text




                                        with db.auto_data.Session() as session:

                                            property = session.query(db.auto_data.car.Property).filter_by(car_id=car.id, name=property_name).first()
                                            if not property:
                                                property = db.auto_data.car.Property(car_id=car.id, name=property_name)
                                                session.add(property)
                                                session.commit()
                                            else:
                                                property.value = property_value
                                                session.commit()




                                        print(f'{property_name} : {property_value}')


                                    except Exception as e:
                                        continue
                                print('------------------------------------------------')

                                vehicle_browser.quit()

                            except Exception as e:
                                print(e)
                                pass
                            

                        sub_model_borwser.quit()

                    model_browser.quit()

                model_category_browser.quit()
            
            browser.quit()
            break
                     
        except:
            print(traceback.format_exc())
            pass




if __name__ == "__main__":

    main()
