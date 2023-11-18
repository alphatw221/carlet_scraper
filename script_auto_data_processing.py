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
from sqlalchemy import not_

# SIMPLIFY_TIRE_SIZE = 'simplify_tire_size'
# SIMPLIFY_FRONT_TIRE_SIZE = 'simplify_front_tire_size'
# SIMPLIFY_REAR_TIRE_SIZE = 'simplify_rear_tire_size'

SIMPLIFY_TIRE_SIZE = 'simplify_tire_size_2'
SIMPLIFY_FRONT_TIRE_SIZE = 'simplify_front_tire_size_2'
SIMPLIFY_REAR_TIRE_SIZE = 'simplify_rear_tire_size_2'

def extract_year_range(input_string):
    # 使用正規表達式，匹配形如 "xxxx - xxxx" 的年份格式
    pattern = re.compile(r'(\d{4})\s*-\s*(\d{4})?')
    # 使用 search 函數找到匹配的部分
    match = pattern.search(input_string)
    
    if match:
        # 如果匹配成功，取得匹配的年份部分
        start_year = int(match.group(1)) if match.group(1) else None
        end_year = int(match.group(2)) if match.group(2) else None
        return start_year, end_year
    else:
        # 如果沒有匹配成功，返回 None
        return None, None


def reformat(match):
    match = re.match(r'(\d{3}/\d{2})\s*([A-Z]+)\s*(\d{2})', match)

    formatted_spec = ''
    if match:
        groups = match.groups()
        # formatted_spec = f"{groups[1]}{groups[2]} {groups[0]} "
        formatted_spec = f" {groups[0]}/{groups[2]} "

    return formatted_spec


def extract_tire_sizes(input_string):
    # 使用正規表達式，匹配形如 "xxx/xx Rxx" 的格式
    # pattern = re.compile(r'\b(\d{3}/\d{2} R\d{2})\b')

    pattern = re.compile(r'(\d{3}/\d{2}\s*[A-Z]+\s*\d{2})')
    matches = pattern.findall(input_string)


    return [reformat(match) for match in matches]



    # 使用 findall 函數找到匹配的部分
    matches = pattern.findall(input_string)
    
    return matches

def main():
    
    with db.auto_data.Session() as session:
        # vehicles= session.query(db.local_carlet.models.Vehicle).filter(db.local_carlet.models.Vehicle.make.in_(target_makes)).order_by(db.local_carlet.models.Vehicle.id.asc()).limit(50)
        cars= session.query(db.auto_data.car.Car).filter_by(start_of_perduction_year=None, end_of_perduction_year=None).yield_per(100)

                              
    for car in cars:
        try:

            make = car.make
            model = car.model
            sub_model = car.sub_model

            start_of_perduction_year, end_of_perduction_year = extract_year_range(sub_model)



            with db.auto_data.Session() as session:
                session.query(db.auto_data.car.Car).filter_by(id=car.id).update({'start_of_perduction_year': start_of_perduction_year, 'end_of_perduction_year': end_of_perduction_year})
                session.commit()

            print('-------------Vehivle----------------')
            print(f'Make : {make}')
            print(f'Model : {model}')
            print(f'Submodel : {sub_model}')
            print(f'Sart of perduction year : {start_of_perduction_year}')
            print(f'End of perduction year : {end_of_perduction_year}')
            print('--------------------------------')




            pass
        except:
            print(traceback.format_exc())
            continue



def store_tire_size_data(car_id, original_tire_size, property_name):
    

    matches = extract_tire_sizes(original_tire_size)

    for match in matches:
        print(match)
        with db.auto_data.Session() as session:
            _property = session.query(db.auto_data.car.Property).filter_by(car_id=car_id, name=property_name, value=match).first()
            if not _property:
                _property = db.auto_data.car.Property(car_id=car_id, name=property_name, value=match)
                session.add(_property)
                session.commit()
        print('-------------Properties----------------')
        print(f'Simplify {property_name} : {match}')
        print('--------------------------------')

def map_tire_size():
    
    with db.auto_data.Session() as session:
        properties= session.query(db.auto_data.car.Property).filter_by(name='Tires size').filter(not_(db.auto_data.car.Property.value.contains('Front wheel tires'))).yield_per(100)
                              
    for property in properties:
        try:
            original_tire_size = property.value


            print('-------------Vehivle----------------')
            print(f'Car ID : {property.car_id}')
            print(f'Original Tire Size : {original_tire_size}')
            print('--------------------------------')
            
            matches = extract_tire_sizes(original_tire_size)
   
            for match in matches:
                print(match)
                with db.auto_data.Session() as session:
                    _property = session.query(db.auto_data.car.Property).filter_by(car_id=property.car_id, name=SIMPLIFY_TIRE_SIZE, value=match).first()
                    if not _property:
                        _property = db.auto_data.car.Property(car_id=property.car_id, name=SIMPLIFY_TIRE_SIZE, value=match)
                        session.add(_property)
                        session.commit()
                print('-------------Properties----------------')
                print(f'Simplify Tire Size : {match}')
                print('--------------------------------')
        except:
            print(traceback.format_exc())
            continue
        
    with db.auto_data.Session() as session:
        properties= session.query(db.auto_data.car.Property).filter_by(name='Tires size').filter(db.auto_data.car.Property.value.contains('Front wheel tires')).yield_per(100)

                              
    for property in properties:
        try:
            original_tire_size = property.value


            print('-------------Vehivle----------------')
            print(f'Car ID : {property.car_id}')
            print(f'Original Tire Size : {original_tire_size}')
            print('--------------------------------')
            
            i = original_tire_size.find('Front wheel tires')
            j = original_tire_size.find('Rear wheel tires')

            original_front_tire_size = original_tire_size[i:j]
            original_rear_tire_size = original_tire_size[j:]

            store_tire_size_data(property.car_id, original_front_tire_size, SIMPLIFY_FRONT_TIRE_SIZE)
            store_tire_size_data(property.car_id, original_rear_tire_size, SIMPLIFY_REAR_TIRE_SIZE)


        except:
            print(traceback.format_exc())
            continue



if __name__ == "__main__":

    map_tire_size()
