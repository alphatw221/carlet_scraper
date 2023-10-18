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

    browser.get("https://www.paintscratch.com/touch_up_paint/")
   
    time.sleep(5)
    return browser





def get_make_links(browser:webdriver.Chrome):
    while True:
        try:
            make_links = browser.find_elements(By.XPATH,f".//div[@class='panel-body']/div[@class='list-group row']/a")
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
            WebDriverWait(make_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'panel-body')))
            break
        except Exception as e:
            print(e)
            make_browser.quit()

    return make_browser

def get_year_links(browser:webdriver.Chrome):
    while True:
        try:
            year_panel = browser.find_element(By.XPATH,f".//div[@class='panel panel-default panel-linklist']")
            year_links = year_panel.find_elements(By.XPATH,f".//div[@class='panel-body']/div[@class='list-group row']/a")
            break
        except Exception as e:
            print(e)
    return year_links

def initYearBrowser(url):
    while True:
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
            yearl_browser = webdriver.Chrome(options=options)
            yearl_browser.get(url)
            WebDriverWait(yearl_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'panel-body')))
            break
        except Exception as e:
            print(e)
            yearl_browser.quit()

    return yearl_browser

def get_model_links(browser:webdriver.Chrome):
    while True:
        try:
            model_links = browser.find_elements(By.XPATH,f".//div[@class='panel-body']/div[@class='list-group row']/a")
            break
        except Exception as e:
            print(e)
    return model_links

def initModelBrowser(url):

    options = webdriver.ChromeOptions()
    options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    model_browser = webdriver.Chrome(options=options)
    model_browser.get(url)
    WebDriverWait(model_browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'breadcrumb')))

    return model_browser

def main():

    while True:
        try:

            previous_make, previous_year, previous_model = '','',''

            with db.paintscratch.Session() as session:
                previous_car = session.query(db.paintscratch.car.Car).order_by(db.paintscratch.car.Car.updated_at.desc()).first()
                if previous_car:
                    previous_make, previous_year, previous_model = previous_car.make, str(previous_car.year), previous_car.model


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

                make_browser = initMakeBrowser(url)
                year_links = get_year_links(make_browser)

                years = []
                for year_link in year_links:
                    if previous_year:
                        if year_link.text == previous_year:
                            years.append({'year':year_link.text,'url':year_link.get_property('href')})
                            previous_year = ''
                        else:
                            continue
                    else:
                        years.append({'year':year_link.text,'url':year_link.get_property('href')})


                for year in years:
                    _year = year.get('year')
                    url = year.get('url')

                    year_browser = initYearBrowser(url)
                    model_links = get_model_links(year_browser)

                    models = []
                    for model_link in model_links:
                        if previous_model:
                            if model_link.text == previous_model:
                                models.append({'name':model_link.text, 'url': make_link.get_attribute('href')})
                                previous_model = ''
                            else:
                                continue
                        else:
                            models.append({'name':model_link.text,'url':model_link.get_property('href')})

                            

                    for model in models:

                        try:
                            model_name = model.get('name')
                            model_url = model.get('url')
                            model_borwser = initModelBrowser(model_url)
                            

                            with db.paintscratch.Session() as session:
                                session.expire_on_commit=False
                                
                                car = session.query(db.paintscratch.car.Car).filter_by(
                                    make=make_name, year=int(_year), model=model_name).first()
                                if not car:
                                    car = db.paintscratch.car.Car(make=make_name, year=int(_year), model=model_name)
                                    session.add(car)
                                    session.commit()

                                session.expunge(car)
                                db.liqui_moly.make_transient(car)

                            print('-------Car-------')
                            print(make_name)
                            print(_year)
                            print(model_name)
                            print('--------------------')




                            li_elements = model_borwser.find_elements(By.XPATH, ".//ul[@class='list-group list-colors']/li")
                            

                            for li_element in li_elements:
                                try:
                                    p_elements = li_element.find_elements(By.XPATH, ".//div[@class='col-sm-7 color-name-code']/p")

                                    color_name = p_elements[0].text
                                    color_code = p_elements[1].text


                                    print('--Paint--')
                                    print(color_name)
                                    print(color_code)
                                    print('---------')
                                    

                                    with db.paintscratch.Session() as session:
                                        paint = session.query(db.paintscratch.car.Paint).filter_by(car_id = car.id, color=color_name, code=color_code).first()
                                        if not paint:
                                            paint = db.paintscratch.car.Paint(car_id=car.id, color=color_name, code=color_code)
                                            session.add(paint)
                                            session.commit()



                                except Exception as e:
                                    print(e)
                                    continue
                            
                            model_borwser.quit()
                            
                        except Exception as e:
                            continue

                    year_browser.quit()

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