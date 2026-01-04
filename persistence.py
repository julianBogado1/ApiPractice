from pymongo import MongoClient
from datetime import datetime
from pprint import pprint
from pydantic import BaseModel

client = MongoClient('localhost', 27017)

class User(BaseModel):
    name: str
    email: str
    bands: list
    user_id: int
#create new user: user = User(name=jack, email=email@itba, ...)
#unpack: user = User(**user_data) ----> user_data = {name: name, email=email, ...} si ya tenia el diccionario lo puedo explotar

users_col = client['test']['users']

async def create_user(user: User):
    users_col.insert_one(user.model_dump())

async def add_band(user_id:int, band:str):
    filter = {"user_id": user_id}
    update = {"$push" : {"bands": band}}
    users_col.update_one(filter, update)

#oyentes de bandas que tengan id mayor a 1 (para complicarla)
async def band_listeners():
    pipeline = [
        {"$match":{"user_id":{"$gt":1}}},
        {"$unwind": "$bands"},
        {"$group":{
                    "_id": "$bands",
                    "listeners": {"$addToSet": "$name"}
                }
        }
    ]
    cursor = users_col.aggregate(pipeline)
    return cursor.to_list(length=None)

if __name__ == "__main__":
    user_data = {
    "name": "julian",
    "email": "mail@mail",
    "bands": ["Guns", "Metallica"],
    "user_id": 1
    }
    # create_user(User(**user_data))
    add_band(1, 'SRV')