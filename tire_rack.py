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

def show_home_page_modal(browser:webdriver.Chrome):



    # responsiveInfoBox('/modalPopups/changeSearchLayer.jsp?noTrack=true','');linkTracking({linkName:'tr: home: shop other products'}); 

    # browser.execute_script("responsiveInfoBox('/modalPopups/changeSearchLayer.jsp?noTrack=true','');linkTracking({linkName:'tr: home: shop other products'});")

    try:
        btn = browser.find_element(By.XPATH,'//div[@id="homeHero"]//div[@class="heroButtonContainer"]/button')
        print(btn)
        try:
            btn.click()
        except :
            browser.execute_script("arguments[0].click();", btn)
    except Exception as e:
        print(e)
    time.sleep(10)

def show_modal(browser:webdriver.Chrome):
    try:
        a = browser.find_element(By.XPATH,'//section[@id="vehicleBar"]//span[@class="vehicleBarDetail"]/a')
        browser.execute_script("arguments[0].click();", a)
    except Exception as e:
        print(e)
    time.sleep(10)

def select_target_vehicle(browser:webdriver.Chrome, make, year, model, additional=''):
        while True:
            try:
                vehicle_brand_select = Select(browser.find_element(By.ID, "vehicle-make"))
                vehicle_brand_select.select_by_visible_text(make)
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(5)
            time.sleep(5)   

        while True:
            try:
                vehicle_year_select = Select(browser.find_element(By.ID, "vehicle-year"))
                vehicle_year_select.select_by_visible_text(year)
                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(5)
            time.sleep(5)

        while True:
            try:
                vehicle_model_select = Select(browser.find_element(By.ID, "vehicle-model"))
                vehicle_model_select.select_by_visible_text(model)

                break
            except Exception as e:
                print(traceback.format_exc())
                time.sleep(5)
            time.sleep(5)
        
        if additional:
            for _ in range(3):
                try:
                    additional_select = Select(browser.find_element(By.ID, "model-add-info"))
                    additional_select.select_by_visible_text(additional)
                    break
                except Exception as e:
                    print(traceback.format_exc())
                    time.sleep(5)

def input_zip_code(browser:webdriver.Chrome):
    
    while True:
        try:
            zip_code_input = browser.find_element(By.ID, "zip-code-vehicle")
            zip_code_input.send_keys('10001')
            break
        except Exception as e:
            print(e)
            time.sleep(5)
    time.sleep(1)


def select_product(browser:webdriver.Chrome, product):

    # 'Tires'
    # 'Wipers'
    while True:
        try:
            vehicle_product_select = Select(browser.find_element(By.ID, "shoppingForSelector"))
            vehicle_product_select.select_by_visible_text(product)
            break
        except Exception as e:
            print(e)
            time.sleep(5)
    time.sleep(1)

def view_results(browser:webdriver.Chrome):

    while True:
        try:
            btn = Select(browser.find_element(By.ID, "shopVehicleSearchBtn"))
            browser.execute_script("arguments[0].click();", btn)
            break
        except Exception as e:
            print(e)
            time.sleep(5)
    time.sleep(10)


       
    

def process_tire():
    pass

def process_wiper():
    pass

def process(browser:webdriver.Chrome, make, year, model, additional=''):

    show_modal(browser)
    select_target_vehicle(browser, make, year, model, additional)
    input_zip_code()
    select_product('Tires')
    view_results(browser)
    process_tire()

    show_modal(browser)
    input_zip_code()
    select_product('Wipers')
    view_results(browser)
    process_wiper()

def main():

    while True:
        try:
            previous_make = 'BMW'
            previous_year = None
            previous_model = None
            previous_additional = None
            
            with db.tire_rack.Session() as session:
                previous_car = session.query(db.tire_rack.car.Car).order_by(db.tire_rack.car.Car.updated_at.desc()).first()
                if previous_car:
                    previous_make, previous_year, previous_model = previous_car.make, previous_car.year, previous_car.model

            browser = init_browser()


            show_home_page_modal(browser)

            time.sleep(20)

            vehicle_brand_select = Select(browser.find_element(By.ID, "vehicle-make"))
            vehicle_brands = ['','BMW','Alfa Romeo', 'Aston Martin','Audi','Ford','Honda','Hyundai','Isuzu','Jaguar',
                              'Jeep','Kia','Land Rover','Lexus','Maybach','Mazda','McLaren','Mercedes-Benz','Mercedes-Maybach',
                              'MINI','Mitsubishi','Nissan','Rivian','Rolls-Royce','Saab','smart','Subaru','Suzuki','Tesla','Toyota',
                              'Volkswagen','Volvo']
            try:
                i = vehicle_brands.index(previous_make) if previous_make else 1
            except:
                i = 1
            previous_make = ''

            for vehicle_brand in vehicle_brands[i:]:

                while True:
                    try:
                        vehicle_brand_select = Select(browser.find_element(By.ID, "vehicle-make"))
                        vehicle_brand_select.select_by_visible_text(vehicle_brand)
                        break
                    except Exception as e:
                        print(traceback.format_exc())
                        time.sleep(5)
                time.sleep(5)   

                vehicle_year_select = Select(browser.find_element(By.ID, "vehicle-year"))
                vehicle_years = [op.text for op in vehicle_year_select.options]

                try:
                    j = vehicle_years.index(previous_year) if previous_year else 1
                except:
                    j = 1
                previous_year = None

                for vehicle_year in vehicle_years[j:]:

                    while True:
                        try:
                            vehicle_year_select = Select(browser.find_element(By.ID, "vehicle-year"))
                            vehicle_year_select.select_by_visible_text(vehicle_year)
                            break
                        except Exception as e:
                            print(traceback.format_exc())
                            time.sleep(5)
                    time.sleep(5)

                    vehicle_model_select = Select(browser.find_element(By.ID, "vehicle-model"))
                    vehicle_models = [op.text for op in vehicle_model_select.options]

                    # model-add-info
                    try:
                        k = vehicle_models.index(previous_model) if previous_model else 1
                    except:
                        k = 1
                    previous_model = ''

                    for vehicle_model in vehicle_models[k:]:

                        while True:
                            try:
                                vehicle_model_select = Select(browser.find_element(By.ID, "vehicle-model"))
                                vehicle_model_select.select_by_visible_text(vehicle_model)

                                break
                            except Exception as e:
                                print(traceback.format_exc())
                                time.sleep(5)

                        

                        try:
                            additional_select = Select(browser.find_element(By.ID, "model-add-info"))
                            additionals = [op.text for op in additional_select.options]
                        except Exception as e:
                            additionals = []

                        if additionals:
                            try:
                                l = additionals.index(previous_additional) if previous_additional else 1
                            except:
                                l = 1
                            previous_additional = ''

                            for additional in additionals[l:]:

                                while True:
                                    try:
                                        additional_select = Select(browser.find_element(By.ID, "model-add-info"))
                                        additional_select.select_by_visible_text(additional)
                                        break
                                    except Exception as e:
                                        print(traceback.format_exc())
                                        time.sleep(5)
                                process(browser, vehicle_brand, vehicle_year, vehicle_model, additional)

                        else:
                            process(browser, vehicle_brand, vehicle_year, vehicle_model, additional)



                     
        except:
            print(traceback.format_exc())
            pass


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
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'productInfo')))
    
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


def test():
    

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

            browser = init_browser()
            getTireData(browser, car, make, model, year, additional)
            browser.quit()

            browser = init_browser()
            getWiperData(browser, car, make, model, year, additional)
            browser.quit()

            with db.tire_rack.Session() as session:
                car= session.query(db.tire_rack.car.Car).filter_by(id=car.id).first()
                car.scraped_at = datetime.utcnow()
                session.commit()
            

        except Exception as e:
            browser.quit()
            print(e)
            continue

        return
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

    # main()
    test()