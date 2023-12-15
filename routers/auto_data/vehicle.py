from typing import Union, List, Annotated
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from pydantic import BaseModel

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate 

from sqlalchemy import select, or_, text, not_
from sqlalchemy.orm import aliased

import lib
import db

from . import router




def get_auto_data_db():
    with db.auto_data.Session() as session:
        yield session


class AutoDataVehicleOut(BaseModel):
    id:int
    make: str
    model: str
    start_of_production_year:int|None
    end_of_production_year:int|None
    sub_model: str
    property_name:str|None
    property_value:str|None
    # properties: List[Property]






@router.get('/vehicles', response_model=Page[AutoDataVehicleOut])
def get_auto_data_vehicles(current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)],
    _db:db.auto_data.Session = Depends(get_auto_data_db), 
                        id:int|str|None=None,
                        make:str|None=None, 
                        model:str|None=None, 
                        sub_model:str|None=None, 
                        start_of_production_year:int|str|None=None,
                        end_of_production_year:int|str|None=None,
                        keyword:str|None=None,
                        order_by:str|None=None):    
 


    car = aliased(db.auto_data.car.Car, name='car')
    property = aliased(db.auto_data.car.Property, name='property')

    query = select(
        car.id, 
        car.make,
        car.model,
        car.sub_model,
        car.start_of_production_year,
        car.end_of_production_year,
        property.name.label('property_name'),
        property.value.label('property_value')
        ).join(property).filter(property.name.in_(['Number of gears and type of gearbox']))
    
    if id and id.isnumeric():
        query = query.filter(car.id==int(id))
    if make:
        query = query.filter(car.make.ilike(f'%{make}%'))
    if start_of_production_year and start_of_production_year.isnumeric():
        query = query.filter(car.start_of_production_year>=int(start_of_production_year))
    if end_of_production_year and end_of_production_year.isnumeric():
        query = query.filter(car.end_of_production_year<int(end_of_production_year))
    if model:
        for sub_string in model.split(','):
            if not sub_string:
                continue
            query = query.filter(car.model.ilike(f'%{sub_string}%'))
    if sub_model:
        for sub_string in sub_model.split(','):
            if not sub_string:
                continue
            query = query.filter(car.sub_model.ilike(f'%{sub_string}%'))
    if keyword:
        query = query.filter(or_(
            car.make.ilike(f'%{keyword}%'), 
            car.model.ilike(f'%{keyword}%'),
            car.sub_model.ilike(f'%{keyword}%'),
        ))


    if order_by:
        order_by_list = order_by.split(',')
        for _order_by in order_by_list:
            asc = True

            if not _order_by:
                continue

            if _order_by[0] == '-' :
                
                if len(_order_by)<=1:
                    continue
                asc = False
                _order_by = _order_by[1:]

            if asc:
                query = query.order_by(text(f'{_order_by} ASC'))
            else:
                query = query.order_by(text(f'{_order_by} DESC'))


    print(query)
    return paginate(_db, query)


