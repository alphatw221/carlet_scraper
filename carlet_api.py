from typing import Union, List, Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# from pydantic import BaseModel
from pydantic import BaseModel

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

import db

from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate 

from sqlalchemy import select, or_, text, not_
from sqlalchemy.orm import aliased

import re


def is_number(s):
    return bool(re.match(r'^-?\d+(?:\.\d+)?$', s))


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

fake_users_db = {
    "carlet": {
        "username": "carlet",
        "full_name": "carlet",
        "email": "carlet@carlet.com.tw",
        "hashed_password": "fakehashed12341234",
        "disabled": False,
    },
}






def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/carlet/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/carlet/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user






def get_carlet_db():
    with db.local_carlet.Session() as session:
        yield session

def get_auto_data_db():
    with db.auto_data.Session() as session:
        yield session

def get_tire_rack_db():
    with db.tire_rack.Session() as session:
        yield session

class CarletVehicleOut(BaseModel):
    id: int|None
    make: str|None
    name: str|None
    year: int|None
    name_variant: str|None
    transmission:str|None
    engine: str|None
    chassis: str|None

    hp: str|None

    auto_data_id: int|None
    tire_rack_id: int|None
    yahoo_id: str|None

class Property(BaseModel):
    name:str|None
    value:str|None
class AutoDataVehicleOut(BaseModel):
    id:int
    make: str
    model: str
    start_of_production_year:int|None
    end_of_production_year:int|None
    sub_model: str
    # properties: List[Property]

class YahooVehicleOut(BaseModel):
    id:int
    make: str
    model: str
    sub_model: str

    # price: float|None
    hp: str|None
    displacement: str|None
    

class TireRackVehicleOut(BaseModel):
    id:int
    make: str
    model: str
    # start_of_perduction_year:int|None
    # end_of_perduction_year:int|None
    sub_model: str
    year:int|None

# @app.get('/users', response_model=Page[db.local_carlet.models.Vehicle])  # use Page[UserOut] as response model
# async def get_users():
#     return paginate(users)  # use paginate function to paginate your data


@app.get('/carlet/vehicles', response_model=Page[CarletVehicleOut])
def get_carlet_vehicles(current_user: Annotated[User, Depends(get_current_active_user)],
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

    query = select(
        vehicle_model.id, 
        vehicle_make.name.label('make'),
        vehicle_model.year, 
        vehicle_model.name, 
        vehicle_model.name_variant, 
        vehicle_model.transmission,
        vehicle_model.engine,
        vehicle_model.chassis,
        vehicle_model.hp,
        vehicle_model.auto_data_id, 
        vehicle_model.tire_rack_id, 
        vehicle_model.yahoo_id, 

        )\
        .join(vehicle_make)
    if id and id.isnumeric():
        query = query.filter(vehicle_model.id==int(id))

    if auto_data_id and is_number(auto_data_id):
        query = query.filter(vehicle_model.auto_data_id==int(auto_data_id))
    if tire_rack_id and is_number(tire_rack_id):
        query = query.filter(vehicle_model.tire_rack_id==int(tire_rack_id))
    if yahoo_id and is_number(yahoo_id):
        query = query.filter(vehicle_model.yahoo_id==int(yahoo_id))
    if make:
        query = query.filter(vehicle_make.name.ilike(f'%{make}%'))
    if start_of_production_year and start_of_production_year.isnumeric():
        query = query.filter(vehicle_model.year>=int(start_of_production_year))
    if end_of_production_year and end_of_production_year.isnumeric():
        query = query.filter(vehicle_model.year<int(end_of_production_year))
    if model:
        for sub_string in model.split(','):
            if not sub_string:
                continue
            query = query.filter(vehicle_model.name.ilike(f'%{sub_string}%'))
    if exclude_model:
        for sub_string in exclude_model.split(','):
            if not sub_string:
                continue
            query = query.filter(not_(vehicle_model.name.ilike(f'%{sub_string}%')))
    if sub_model:
        for sub_string in sub_model.split(','):
            if not sub_string:
                continue
            query = query.filter(vehicle_model.name_variant.ilike(f'%{sub_string}%'))
    if exclude_sub_model:
        print(exclude_sub_model)
        for sub_string in exclude_sub_model.split(','):
            if not sub_string:
                continue
            query = query.filter(not_(vehicle_model.name_variant.ilike(f'%{sub_string}%')))
    if keyword:
        query = query.filter(or_(
            vehicle_make.name.label('make').ilike(f'%{keyword}%'), 
            vehicle_model.name.ilike(f'%{keyword}%'),
            vehicle_model.variant.ilike(f'%{keyword}%'),
            vehicle_model.name_variant.ilike(f'%{keyword}%'),
            vehicle_model.engine.ilike(f'%{keyword}%'),
            vehicle_model.chassis.ilike(f'%{keyword}%'),
        ))
    if engine:
        query = query.filter(vehicle_model.engine.ilike(f'%{engine}%'))
    if chassis:
        query = query.filter(vehicle_model.chassis.ilike(f'%{chassis}%'))
    if exclude_auto_data_done_mapping == 'true':
        query = query.filter(vehicle_model.auto_data_id==None)

    if exclude_tire_rack_done_mapping == 'true':
        query = query.filter(vehicle_model.tire_rack_id==None)

    if exclude_yahoo_done_mapping == 'true':
        query = query.filter(vehicle_model.yahoo_id==None)

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





@app.get('/carlet/auto_data/vehicles', response_model=Page[AutoDataVehicleOut])
def get_auto_data_vehicles(current_user: Annotated[User, Depends(get_current_active_user)],
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

    query = select(
        car.id, 
        car.make,
        car.model,
        car.sub_model,
        car.start_of_production_year,
        car.end_of_production_year,
        )
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



    return paginate(_db, query)




@app.get('/carlet/yahoo/vehicles', response_model=Page[YahooVehicleOut])
def get_yahoo_vehicles(current_user: Annotated[User, Depends(get_current_active_user)],
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



@app.get('/carlet/tire_rack/vehicles', response_model=Page[TireRackVehicleOut])
def get_tire_rack_vehicles(current_user: Annotated[User, Depends(get_current_active_user)],
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


add_pagination(app)  # important! add pagination to your app


class AutoDataVehicle(BaseModel):
    auto_data_vehicle_id: int|str|None


@app.put("/carlet/vehicle/{carlet_vehicle_id}/mapping/auto_data")
def update_carlet_vehicle_auto_data_id(
    current_user: Annotated[User, Depends(get_current_active_user)],
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


@app.put("/carlet/vehicle/{carlet_vehicle_id}/mapping/tire_rack")
def update_carlet_vehicle_tire_rack_id(
    current_user: Annotated[User, Depends(get_current_active_user)], 
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


@app.put("/carlet/vehicle/{carlet_vehicle_id}/mapping/yahoo")
def update_carlet_vehicle_yahoo_id(
    current_user: Annotated[User, Depends(get_current_active_user)], 
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

@app.put("/carlet/vehicle/{carlet_vehicle_id}/update")
def update_carlet_vehicle(
    current_user: Annotated[User, Depends(get_current_active_user)], 
    carlet_vehicle_id: int, 
    data: updateVehicleData):

    with db.local_carlet.Session() as session:

                            
        car = session.query(db.local_carlet.models.VehicleModel).filter_by(id=carlet_vehicle_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Vehidle Not Found")
        
        car.hp = data.hp if data.hp else None
        session.commit()

    return 'ok'














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

# poetry run uvicorn carlet_api:app --host 0.0.0.0 --port 8000
#http://127.0.0.1:8000/docs
#http://127.0.0.1:8000/redoc





