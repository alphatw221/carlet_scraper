from typing import Union, List, Annotated

from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate 

from pydantic import BaseModel,validator

from sqlalchemy import select, or_, text, not_
from sqlalchemy.orm import aliased,selectinload

import lib
import db



router = APIRouter(prefix='/vehicles')



def get_carlet_db():
    with db.local_carlet.Session() as session:
        yield session

class Make(BaseModel):
    name:str|None
class CarletVehicleOut(BaseModel):
    id: int|None
    make_id:int|None
    make: Make|None
    make_name: str = ""  # 新增 make_name 的欄位

    name: str|None
    year: int|None
    name_variant: str|None
    trim_level: str|None
    fuel: str|None
    displacement: int|None
    transmission:str|None
    size: str|None
    engine: str|None
    chassis: str|None
    hp: str|None
    auto_data_id: int|None
    tire_rack_id: int|None
    yahoo_id: str|None

    supported: int|None
    is_show: int|None


    class Config:
        orm_mode = True

    @validator("make_name", pre=True, always=True)
    def extract_make_name(cls, value, values):

        try:
            return values.get("make", {}).name
        except Exception as e:
            print(e)
        return ''

class Property(BaseModel):
    name:str|None
    value:str|None
 
    



@router.get('/', response_model=Page[CarletVehicleOut])
def get_carlet_vehicles(current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)],
        _db:db.local_carlet.Session = Depends(get_carlet_db), 
                        id:str|None=None,
                        make:str|None=None, 
                        start_of_production_year:int|str|None=None,
                        end_of_production_year:int|str|None=None,
                        model:str|None=None, 
                        exclude_model:str|None=None, 
                        sub_model:str|None=None,
                        exclude_sub_model:str|None=None,
                        keyword:str|None=None,
                        engine:str|None=None,
                        chassis:str|None=None,
                        exclude_auto_data_done_mapping:str|None=None,
                        exclude_tire_rack_done_mapping:str|None=None,
                        exclude_yahoo_done_mapping:str|None=None,
                        order_by:str|None=None,
                        auto_data_id:str|None=None,
                        tire_rack_id:str|None=None,
                        yahoo_id:str|None=None,
                        ):    
    
    vehicle_model = aliased(db.local_carlet.models.VehicleModel, name='vehicle_model')
    vehicle_make = aliased(db.local_carlet.models.VehicleMake, name='vehicle_make')

    # query = select(
    #     vehicle_model.id, 
    #     vehicle_make.name.label('make'),
    #     vehicle_model.year, 
    #     vehicle_model.name, 
    #     vehicle_model.name_variant, 
    #     vehicle_model.transmission,
    #     vehicle_model.engine,
    #     vehicle_model.chassis,
    #     vehicle_model.hp,
    #     vehicle_model.auto_data_id, 
    #     vehicle_model.tire_rack_id, 
    #     vehicle_model.yahoo_id, 

    #     )\
    #     .join(vehicle_make)
    
    vehicles = _db.query(db.local_carlet.models.VehicleModel).join(db.local_carlet.models.VehicleMake).options(selectinload(db.local_carlet.models.VehicleModel.make))

    if id and id.isnumeric():
        # query = query.filter(vehicle_model.id==int(id))
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.id==int(id))
    if auto_data_id and lib.utils.is_number(auto_data_id):
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.auto_data_id==int(auto_data_id))

        # query = query.filter(vehicle_model.auto_data_id==int(auto_data_id))
    if tire_rack_id and lib.utils.is_number(tire_rack_id):
        # query = query.filter(vehicle_model.tire_rack_id==int(tire_rack_id))
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.tire_rack_id==int(tire_rack_id))
    if yahoo_id and lib.utils.is_number(yahoo_id):
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.yahoo_id==int(yahoo_id))
        # query = query.filter(vehicle_model.yahoo_id==int(yahoo_id))
    if make:
        vehicles = vehicles.filter(db.local_carlet.models.VehicleMake.name.ilike(f'%{make}%'))
        # query = query.filter(vehicle_make.name.ilike(f'%{make}%'))
    if start_of_production_year and start_of_production_year.isnumeric():
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.year>=int(start_of_production_year))
        # query = query.filter(vehicle_model.year>=int(start_of_production_year))
    if end_of_production_year and end_of_production_year.isnumeric():
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.year<int(end_of_production_year))
        # query = query.filter(vehicle_model.year<int(end_of_production_year))
    if model:
        for sub_string in model.split(','):
            if not sub_string:
                continue
            vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.name.ilike(f'%{sub_string}%'))
            # query = query.filter(vehicle_model.name.ilike(f'%{sub_string}%'))
    if exclude_model:
        for sub_string in exclude_model.split(','):
            if not sub_string:
                continue
            vehicles = vehicles.filter(not_(db.local_carlet.models.VehicleModel.name.ilike(f'%{sub_string}%')))
            # query = query.filter(not_(vehicle_model.name.ilike(f'%{sub_string}%')))
    if sub_model:
        for sub_string in sub_model.split(','):
            if not sub_string:
                continue
            vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.name_variant.ilike(f'%{sub_string}%'))
            # query = query.filter(vehicle_model.name_variant.ilike(f'%{sub_string}%'))
    if exclude_sub_model:
        print(exclude_sub_model)
        for sub_string in exclude_sub_model.split(','):
            if not sub_string:
                continue
            vehicles = vehicles.filter(not_(db.local_carlet.models.VehicleModel.name_variant.ilike(f'%{sub_string}%')))
            # query = query.filter(not_(vehicle_model.name_variant.ilike(f'%{sub_string}%')))
    # if keyword:
    #     query = query.filter(or_(
    #         vehicle_make.name.label('make').ilike(f'%{keyword}%'), 
    #         vehicle_model.name.ilike(f'%{keyword}%'),
    #         vehicle_model.variant.ilike(f'%{keyword}%'),
    #         vehicle_model.name_variant.ilike(f'%{keyword}%'),
    #         vehicle_model.engine.ilike(f'%{keyword}%'),
    #         vehicle_model.chassis.ilike(f'%{keyword}%'),
    #     ))
    if engine:
        # query = query.filter(vehicle_model.engine.ilike(f'%{engine}%'))
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.engine.ilike(f'%{engine}%'))
    if chassis:
        # query = query.filter(vehicle_model.chassis.ilike(f'%{chassis}%'))
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.chassis.ilike(f'%{chassis}%'))
    if exclude_auto_data_done_mapping == 'true':
        # query = query.filter(vehicle_model.auto_data_id==None)
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.auto_data_id==None)
    if exclude_tire_rack_done_mapping == 'true':
        # query = query.filter(vehicle_model.tire_rack_id==None)
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.tire_rack_id==None)
    if exclude_yahoo_done_mapping == 'true':
        # query = query.filter(vehicle_model.yahoo_id==None)
        vehicles = vehicles.filter(db.local_carlet.models.VehicleModel.yahoo_id==None)
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
                vehicles = vehicles.order_by(text(f'vehicle_model_{_order_by} ASC'))
                # query = query.order_by(text(f'vehicle_model_{_order_by} ASC'))
            else:
                vehicles = vehicles.order_by(text(f'vehicle_model_{_order_by} DESC'))
                # query = query.order_by(text(f'vehicle_model_{_order_by} DESC'))

    return paginate(vehicles)
    return paginate(_db, query)






class AutoDataVehicle(BaseModel):
    auto_data_vehicle_id: int|str|None


@router.put("/{carlet_vehicle_id}/mapping/auto_data")
def update_carlet_vehicle_auto_data_id(
    current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)],
    carlet_vehicle_id: int, 
    data: AutoDataVehicle):
    
    print(carlet_vehicle_id)
    print(data.auto_data_vehicle_id)

    with db.local_carlet.Session() as session:
        session.expire_on_commit=False
                            
        car = session.query(db.local_carlet.models.VehicleModel).filter_by(id=carlet_vehicle_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Vehidle Not Found")
        
        car.auto_data_id = data.auto_data_vehicle_id if data.auto_data_vehicle_id else None
        session.commit()

    return 'ok'


class TireRackVehicle(BaseModel):
    tire_rack_vehicle_id: int|str|None


@router.put("/{carlet_vehicle_id}/mapping/tire_rack")
def update_carlet_vehicle_tire_rack_id(
    current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)], 
    carlet_vehicle_id: int, 
    data: TireRackVehicle):

    with db.local_carlet.Session() as session:
        session.expire_on_commit=False
                            
        car = session.query(db.local_carlet.models.VehicleModel).filter_by(id=carlet_vehicle_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Vehidle Not Found")
        
        car.tire_rack_id = data.tire_rack_vehicle_id if data.tire_rack_vehicle_id else None
        session.commit()

    return 'ok'



class YahooVehicle(BaseModel):
    yahoo_vehicle_id: int|str|None


@router.put("/{carlet_vehicle_id}/mapping/yahoo")
def update_carlet_vehicle_yahoo_id(
    current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)], 
    carlet_vehicle_id: int, 
    data: YahooVehicle):
    print(data)
    with db.local_carlet.Session() as session:

                            
        car = session.query(db.local_carlet.models.VehicleModel).filter_by(id=carlet_vehicle_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Vehidle Not Found")
        
        car.yahoo_id = data.yahoo_vehicle_id if data.yahoo_vehicle_id else None
        print(car)
        print(car.yahoo_id)
        session.commit()

    return 'ok'


class updateVehicleData(BaseModel):
    hp: str|None
    chassis: str|None
    displacement: int|None
    engine: str|None
    fuel: str|None
    make_id: int|None
    name_variant: str|None
    name: str|None
    size: str|None
    transmission: str|None
    trim_level: str|None
    year: int|None




@router.put("/{carlet_vehicle_id}/update")
def update_carlet_vehicle(
    current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)], 
    carlet_vehicle_id: int, 
    data: updateVehicleData):

    with db.local_carlet.Session() as session:

                            
        car = session.query(db.local_carlet.models.VehicleModel).filter_by(id=carlet_vehicle_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Vehidle Not Found")
        
        session.query(db.local_carlet.models.VehicleModel).filter_by(id=carlet_vehicle_id).update(dict(data))
        session.commit()

    return 'ok'


class createVehicleData(BaseModel):
    hp: str|None
    chassis: str|None
    displacement: int|None
    engine: str|None
    fuel: str
    make_id: int
    name: str
    name_variant: str
    size: str
    transmission: str
    trim_level: str|None
    year: int
    supported: int
    is_show: int



@router.post("/create")
def create_carlet_vehicle(
    current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)], 
    data: createVehicleData):

    with db.local_carlet.Session() as session:
        vehicle_model = db.local_carlet.models.VehicleModel(**dict(data))

        session.add(vehicle_model)
        session.commit()

      
    return 'ok'

@router.delete("/{carlet_vehicle_id}/delete")
def delete_carlet_vehicle(
    current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)],carlet_vehicle_id ):

    with db.local_carlet.Session() as session:

                            
        car = session.query(db.local_carlet.models.VehicleModel).filter_by(id=carlet_vehicle_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Vehidle Not Found")
        

        session.delete(car)
        session.commit()
      
    return 'ok'