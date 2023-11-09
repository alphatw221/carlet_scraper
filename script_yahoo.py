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

    while True:
        try:
            target_makes = [
                'BMW 寶馬', 
                # 'Audi 奧迪', 
                'M-Benz 賓士', 
                'Porsche 保時捷'
            ]

            previous_make, previous_model, previous_sub_model = '','',''

            with db.local_carlet.Session() as session:
                previous_car = session.query(db.local_carlet.models.Vehicle).filter(db.local_carlet.models.Vehicle.make.in_(target_makes)).order_by(db.local_carlet.models.Vehicle.created_at.desc()).first()
                if previous_car:
                    previous_make,  previous_model, previous_sub_model = previous_car.make, previous_car.model, previous_car.sub_model

            if previous_make and previous_make not in target_makes:
                previous_make, previous_model, previous_sub_model = '','',''

            print(previous_make)
            print(previous_model)
            print(previous_sub_model)

            browser = init_browser()
            make_links = get_make_links(browser)

            makes = []
            for make_link in make_links:
                
                if make_link.text not in target_makes:
                    continue

                if previous_make:
                    if make_link.text == previous_make:
                        makes.append({'name':make_link.text, 'url': make_link.get_attribute('href')})
                        previous_make = ''
                    else:
                        continue
                else:
                    makes.append({'name':make_link.text, 'url': make_link.get_attribute('href')})
            print('Makes :')
            print(makes)
            for make in makes:
                make_name = make.get('name')
                url = make.get('url')

                try:
                    model_browser = initModelBrowser(url)
                except Exception as e:
                    print(traceback.format_exc())
                    continue
                
                print('scroll')
                scroll_all_page(model_browser)

                print('get model links')
                model_links = get_model_links(model_browser)

                models = []
                for model_link in model_links:

                    try:
                        name = model_link.find_element(By.XPATH,".//span[@class='title']").text
                    except Exception as e:
                        print(e)
                        name = ''

                    if previous_model:
                        if name == previous_model:


                            models.append({'name':name, 'url': model_link.get_attribute('href')})
                            previous_model = ''
                        else:
                            continue
                    else:
                        models.append({'name':name,'url':model_link.get_property('href')})

                print('Models :')
                print(models)
                for model in models:

                    model_name = model.get('name')
                    model_url = model.get('url')

                    try:
                        sub_model_borwser = initSubModelBrowser(model_url)
                    except Exception as e:
                        print(traceback.format_exc())
                        continue

                    sub_model_links = get_sub_model_links(sub_model_borwser)
                    
                    print('Submodel Links :')
                    print(sub_model_links)
                    
                    if not sub_model_links:
                        while True:
                            time.sleep(1)

                    sub_models = []
                    
                    for sub_model_link in sub_model_links:
                        
                        try:
                            # name = sub_model_link.find_element(By.XPATH,'./span').text

                            name = sub_model_link.find_element(By.XPATH,".//div[@class='model-title']").text

                        except Exception as e:
                            print(e)
                            name = ''
                        
                        if not name:
                            continue

                        if previous_sub_model:
                            print('Previous Submodel :')
                            print(previous_sub_model)
                            
                            print('Current Submodel :')
                            print(name)
                            if name == previous_sub_model:
                                print('a')

                                sub_models.append({'name':name, 'url': sub_model_link.get_attribute('href')})
                                previous_sub_model = ''
                            else:
                                print('b')

                                continue
                        else:
                            print('c')
                            sub_models.append({'name':name,'url':sub_model_link.get_property('href')})


                    print('Sub Models :')
                    print(sub_models)

                    for sub_model in sub_models:
                        try:
                            sub_model_name = sub_model.get('name')
                            sub_model_link = sub_model.get('url')

                            try:
                                vehicle_browser = initVehicleBrowser((sub_model_link))
                            except Exception as e:
                                print(traceback.format_exc())
                                continue
                            
                            try:
                                price = vehicle_browser.find_element(By.XPATH,f".//div[@class='main']//div[@class='trim-main']//h3[@class='price']/span/font").text
                            except Exception as e:
                                print(e)
                                price = 0

                            try:
                                spec_li_tags = vehicle_browser.find_elements(By.XPATH,f".//div[@class='main']//div[@class='trim-main']//div[@class='trim-spec']//ul[@class='spec-wrapper']//li")
                            except Exception as e:
                                print(e)
                                continue
                            
                            displacement, output = '', ''
                            for spec_li_tag in spec_li_tags:
                                try:
                                    span_tags = spec_li_tag.find_elements(By.XPATH,"./span")

                                    if span_tags[0].text=='性能數據':
                                        output = span_tags[1].text
                                    elif span_tags[0].text=='排氣量':
                                        displacement = span_tags[1].text
                                except Exception as e:
                                    print(e)
                                    continue


                            # trs = vehicle_browser.find_elements(By.XPATH,f".//table[@class='cardetailsout car2']//tr")



                            with db.local_carlet.Session() as session:

                                car = session.query(db.local_carlet.models.Vehicle).filter_by(make=make_name, model=model_name, sub_model=sub_model_name).first()
                                if not car:
                                    car = db.local_carlet.models.Vehicle(make=make_name, model=model_name, sub_model=sub_model_name, price=float(price), output=output, displacement=displacement)
                                    session.add(car)
                                    session.commit()


                            print('-------------------------vehicle----------------')
                            print(f'Make : {make_name}')
                            print(f'Model : {model_name}')
                            print(f'Sub Model : {sub_model_name}')
                            print(f'Price : {price}')
                            print(f'Output : {output}')
                            print(f'displacement : {displacement}')
                            print('------------------------------------------------')
                            # print('-------------------------properties-------------')
                            # for tr in trs:
                            #     try:
                            #         property_name = tr.find_element(By.XPATH,f"./th").text
                            #         property_value = tr.find_element(By.XPATH,f"./td").text
                            #         with db.auto_data.Session() as session:

                            #             property = session.query(db.auto_data.car.Property).filter_by(car_id=car.id, name=property_name).first()
                            #             if not property:
                            #                 property = db.auto_data.car.Property(car_id=car.id, name=property_name, value=property_value)
                            #                 session.add(property)
                            #                 session.commit()
                            #             else:
                            #                 property.value = property_value
                            #                 session.commit()

                            #         print(f'{property_name} : {property_value}')

                            #     except Exception as e:
                            #         continue
                            # print('------------------------------------------------')

                            # vehicle_browser.quit()

                        except Exception as e:
                            print(e)
                            pass
                        

                    sub_model_borwser.quit()

                model_browser.quit()
            
            browser.quit()
            break
                     
        except:
            print(traceback.format_exc())
            pass




if __name__ == "__main__":

    main()
