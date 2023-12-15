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




def get_carlet_db():
    with db.local_carlet.Session() as session:
        yield session


class YahooVehicleOut(BaseModel):
    id:int
    make: str
    model: str
    sub_model: str
    # price: float|None
    hp: str|None
    displacement: str|None
    



@router.get('/carlet/yahoo/vehicles', response_model=Page[YahooVehicleOut])
def get_yahoo_vehicles(current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)],
    _db:db.local_carlet.Session = Depends(get_carlet_db), 
                        id:int|str|None=None,
                        make:str|None=None, 
                        model:str|None=None, 
                        sub_model:str|None=None, 
                        keyword:str|None=None,
                        hp:str|None=None,
                        displacement:str|None=None,
                        order_by:str|None=None):    
 


    vehicle = aliased(db.local_carlet.models.Vehicle, name='vehicle')

    query = select(
        vehicle.id, 
        vehicle.make,
        vehicle.model,
        vehicle.sub_model,
        vehicle.output,
        vehicle.displacement,
        )
    if id and id.isnumeric():
        query = query.filter(vehicle.id==int(id))
    if make:
        query = query.filter(vehicle.make.ilike(f'%{make}%'))
    
    if model:
        for sub_string in model.split(','):
            if not sub_string:
                continue
            query = query.filter(vehicle.model.ilike(f'%{sub_string}%'))
    if sub_model:
        for sub_string in sub_model.split(','):
            if not sub_string:
                continue
            query = query.filter(vehicle.sub_model.ilike(f'%{sub_string}%'))
    if keyword:
        query = query.filter(or_(
            vehicle.make.ilike(f'%{keyword}%'), 
            vehicle.model.ilike(f'%{keyword}%'),
            vehicle.sub_model.ilike(f'%{keyword}%'),
        ))

    if hp:
        query = query.filter(vehicle.output.ilike(f'%{hp}%'))
    if displacement:
        query = query.filter(vehicle.displacement.ilike(f'%{displacement}%'))

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


