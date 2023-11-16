from typing import Union

from fastapi import FastAPI, Depends
# from pydantic import BaseModel
from pydantic import BaseModel

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

import db

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate 

from sqlalchemy import select, or_
from sqlalchemy.orm import aliased



app = FastAPI(middleware=[
    Middleware(CORSMiddleware, 
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],)
])

# app = FastAPI()
# class Car(BaseModel):
#     make:str
#     year:int
#     model:str
#     additional:Union[str,None] = None



def get_carlet_db():
    with db.local_carlet.Session() as session:
        yield session

def get_auto_data_db():
    with db.auto_data.Session() as session:
        yield session


class CarletVehicleOut(BaseModel):
    # id: int|None
    # name_1:str|None
    # name: str|None

    # year: int|None
    # name_variant: str|None
    pass


class AutoDataVehicleVehicleOut(BaseModel):
    
    make: str
    model: str

    start_of_perduction_year:int|None
    end_of_perduction_year:int|None

    sub_model: str



# @app.get('/users', response_model=Page[db.local_carlet.models.Vehicle])  # use Page[UserOut] as response model
# async def get_users():
#     return paginate(users)  # use paginate function to paginate your data


@app.get('/carlet/vehicles', response_model=Page[CarletVehicleOut])
def get_carlet_vehicles(_db:db.local_carlet.Session = Depends(get_carlet_db), 
                        make:str|None=None, 
                        start_of_perduction_year:int|None=None,
                        end_of_perduction_year:int|None=None,
                        name:str|None=None, 
                        keyword:str|None=None,
                        order_by:str|None=None):    
    
    vehicle_model = aliased(db.local_carlet.models.VehicleModel, name='vehicle_model')
    vehicle_make = aliased(db.local_carlet.models.VehicleMake, name='vehicle_make')

    # 连接两个表格
    # query = session.query(table1.name.label('table1_name'), 
    #                     table2.name.label('table2_name')).\
    #         join(table2_alias, table1.name == table2_alias.name)

    # 执行查询

    query = select(vehicle_model, vehicle_make)\
        .join(vehicle_make)\
        # .where(db.local_carlet.models.VehicleModel.make_id==db.local_carlet.models.VehicleMake.id)

    
    if make:
        query = query.filter(vehicle_make.name.contains(make))
    if start_of_perduction_year:
        query = query.filter(vehicle_model.year>=start_of_perduction_year)
    if end_of_perduction_year:
        query = query.filter(vehicle_model.year<end_of_perduction_year)
    if name:
        query = query.filter(vehicle_model.name.contains(name))
    if keyword:
        query = query.filter(or_(
                                    vehicle_make.name.contains(keyword), 
                                    vehicle_model.name.contains(keyword),
                                    vehicle_model.variant.contains(keyword),
                                    vehicle_model.name_variant.contains(keyword),
                                    vehicle_model.engine.contains(keyword),
                                    vehicle_model.chassis.contains(keyword),
                                 ))
    if order_by:
        order_by_list = order_by.split((','))
        for _order_by in order_by_list:
            asc = True
            if _order_by[0] == '-':
                asc = False
                _order_by = _order_by[1:]
                
            if hasattr(db.local_carlet.models.VehicleModel, _order_by) :
                if asc:
                    query = query.order_by(getattr(db.local_carlet.models.VehicleModel, _order_by).asc())
                else:
                    query = query.order_by(getattr(db.local_carlet.models.VehicleModel, _order_by).desc())

            elif hasattr(db.local_carlet.models.VehicleMake, _order_by) :
                if asc:
                    query = query.order_by(getattr(db.local_carlet.models.VehicleMake, _order_by).asc())
                else:
                    query = query.order_by(getattr(db.local_carlet.models.VehicleMake, _order_by).desc())


    print(query)

    
    return paginate(_db, query)





@app.get('/auto_data/vehicles', response_model=Page[AutoDataVehicleVehicleOut])
def get_carlet_vehicles(_db:db.auto_data.Session = Depends(get_auto_data_db), 
                        make:str|None=None, 
                        model:str|None=None, 
                        sub_model:str|None=None, 
                        start_of_perduction_year:int|None=None,
                        end_of_perduction_year:int|None=None,
                        keyword:str|None=None):    

    return paginate(_db, select(db.auto_data.car.Car).order_by(db.auto_data.car.Car.created_at))






add_pagination(app)  # important! add pagination to your app



# @app.post("/vehicle")
# def create_vehicle(car_data: Car):


#     with db.tire_rack.Session() as session:
#         session.expire_on_commit=False
                            
#         car = session.query(db.tire_rack.car.Car).filter_by(make=car_data.make, year=car_data.year, model=car_data.model, sub_model=car_data.additional).first()
#         if not car:
#             car = db.tire_rack.car.Car(make=car_data.make, year=car_data.year, model=car_data.model, sub_model=car_data.additional)
#             session.add(car)
#             session.commit()

#         session.expunge(car)
#         db.tire_rack.make_transient(car)

#         print('**Car**')
#         print(car.make)
#         print(car.year)
#         print(car.model)
#         print(car.sub_model)
#         print('*******')


#     return {"make": car.make, "year": car.year, "model": car.model, "additional": car.sub_model}



# @app.get("/vehicle/latest")
# def get_latest_vehicle():

#     with db.tire_rack.Session() as session:
#         session.expire_on_commit=False

#         previous_car = session.query(db.tire_rack.car.Car).order_by(db.tire_rack.car.Car.created_at.desc()).first()
#         session.expunge(previous_car)
#         db.tire_rack.make_transient(previous_car)

#     if previous_car:
#         return {"make": previous_car.make, "year": previous_car.year, "model": previous_car.model, "additional": previous_car.sub_model}
    
#     return {"make": '', "year": '', "model": '', "additional": ''}
      



# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}




# poetry run uvicorn carlet_api:app --reload
#http://127.0.0.1:8000/docs
#http://127.0.0.1:8000/redoc


