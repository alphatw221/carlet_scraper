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


def init_browser():
    browser = webdriver.Chrome()
    browser.get("https://www.tirerack.com/content/tirerack/desktop/en/homepage.html")
   
    time.sleep(5)
    return browser

def show_home_page_modal(browser:webdriver.Chrome):



    # responsiveInfoBox('/modalPopups/changeSearchLayer.jsp?noTrack=true','');linkTracking({linkName:'tr: home: shop other products'}); 

    browser.execute_script("responsiveInfoBox('/modalPopups/changeSearchLayer.jsp?noTrack=true','');linkTracking({linkName:'tr: home: shop other products'});")

    # try:
    #     btn = browser.find_element(By.XPATH,'//div[@id="homeHero"]//div[@class="heroButtonContainer"]/button')
    #     print(btn)
    #     try:
    #         btn.click()
    #     except :
    #         browser.execute_script("arguments[0].click();", btn)
    # except Exception as e:
    #     print(e)
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


def test():
    browser = init_browser()
    
    # browser = webdriver.Safari()
    # browser.get("https://www.tirerack.com/tires/SelectTireSize.jsp?autoMake=BMW&autoModel=323Ci&autoYear=2000&autoModClar=&perfCat=ALL")
   
    # time.sleep(10)
    # show_modal(browser)
    show_home_page_modal(browser)

    while True:
        pass
if __name__ == "__main__":

    # main()
    test()