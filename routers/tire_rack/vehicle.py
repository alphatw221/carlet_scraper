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

# router = APIRouter(route_class=CarletApiV2Route)

def get_tire_rack_db():
    with db.tire_rack.Session() as session:
        yield session


class TireRackVehicleOut(BaseModel):
    id:int
    make: str
    model: str
    # start_of_perduction_year:int|None
    # end_of_perduction_year:int|None
    sub_model: str
    year:int|None



@router.get('/vehicles', response_model=Page[TireRackVehicleOut])
def get_tire_rack_vehicles(current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)],
    _db:db.tire_rack.Session = Depends(get_tire_rack_db), 
                        id:str|int|None=None,
                        make:str|None=None, 
                        model:str|None=None, 
                        sub_model:str|None=None, 
                        start_of_production_year:str|int|None=None,
                        end_of_production_year:str|int|None=None,
                        keyword:str|None=None,
                        order_by:str|None=None):    
 


    car = aliased(db.tire_rack.car.Car, name='car')
    # property = aliased(db.auto_data.car.Property, name='property')

    query = select(
        car.id, 
        car.make,
        car.model,
        car.sub_model,
        car.year
        # car.start_of_perduction_year,
        # car.end_of_perduction_year,
        )
    if id and id.isnumeric():
        query = query.filter(car.id==int(id))
    if make:
        query = query.filter(car.make.ilike(f'%{make}%'))
    if start_of_production_year and start_of_production_year.isnumeric():
        query = query.filter(car.year>=start_of_production_year)
    if end_of_production_year and end_of_production_year.isnumeric():
        query = query.filter(car.year<end_of_production_year)
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

    return paginate(_db, query)

