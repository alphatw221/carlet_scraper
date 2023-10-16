from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

import db

app = FastAPI(middleware=[
    Middleware(CORSMiddleware, 
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],)
])

# app = FastAPI()
class Car(BaseModel):
    make:str
    year:int
    model:str
    additional:Union[str,None] = None

@app.post("/vehicle")
def create_vehicle(car_data: Car):


    with db.tire_rack.Session() as session:
        session.expire_on_commit=False
                            
        car = session.query(db.tire_rack.car.Car).filter_by(make=car_data.make, year=car_data.year, model=car_data.model, sub_model=car_data.additional).first()
        if not car:
            car = db.tire_rack.car.Car(make=car_data.make, year=car_data.year, model=car_data.model, sub_model=car_data.additional)
            session.add(car)
            session.commit()

        session.expunge(car)
        db.tire_rack.make_transient(car)

        print('**Car**')
        print(car.make)
        print(car.year)
        print(car.model)
        print(car.sub_model)
        print('*******')


    return {"make": car.make, "year": car.year, "model": car.model, "additional": car.sub_model}



@app.get("/vehicle/latest")
def get_latest_vehicle():

    with db.tire_rack.Session() as session:
        session.expire_on_commit=False

        previous_car = session.query(db.tire_rack.car.Car).order_by(db.tire_rack.car.Car.updated_at.desc()).first()
        session.expunge(previous_car)
        db.tire_rack.make_transient(previous_car)

    if previous_car:
        return {"make": previous_car.make, "year": previous_car.year, "model": previous_car.model, "additional": previous_car.sub_model}
    
    return {"make": '', "year": '', "model": '', "additional": ''}
      



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




# poetry run uvicorn tire_rack_api:app --reload
#http://127.0.0.1:8000/docs
#http://127.0.0.1:8000/redoc