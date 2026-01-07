from pymongo import MongoClient
from datetime import datetime
from pprint import pprint
from pydantic import BaseModel
from bson import ObjectId
import random

client = MongoClient('localhost', 27017)

class User(BaseModel):
    user_id: int
    name: str
    email: str
    bands: list[int]
#create new user: user = User(name=jack, email=email@itba, ...)
#unpack: user = User(**user_data) ----> user_data = {name: name, email=email, ...} si ya tenia el diccionario lo puedo explotar


class Band(BaseModel):
    band_id: int
    name: str
    records: list[str]
    assembly: int
    current_state: str


users_col = client['test']['users']
bands_col = client['test']['bands']

async def create_user(user: User) -> int:
    """Persists a user and returns the user_id"""
    #TODO if user exists UserAlreadyExistsException

    users_col.insert_one(user.model_dump())
    return user.user_id

async def get_user(user_id: int) -> User | None:
    """Finds a user given its id"""

    result = users_col.find_one({'user_id': user_id})
    if result is None:
        return None
    return User(**result)

async def create_band(band:Band) -> int:
    """Persists a band and returns the band_id"""
    #TODO if band exists BandAlreadyExistsException

    bands_col.insert_one(band.model_dump())
    return band.band_id

async def get_band(band_id: int) -> Band | None:
    """Finds a band given its id"""

    result = bands_col.find_one({'band_id': band_id})
    if result is None:
        return None
    return Band(**result)


if __name__ == "__main__":

    bands: list[Band] = []

    for i in range(1, 11):
        band = Band(
            band_id=i,
            name=f"Band {i}",
            records=[f"Album {i}-A", f"Album {i}-B"],
            assembly=2000 + i,
            current_state="active" if i % 2 == 0 else "inactive"
        )
        bands.append(band)

    bands_col.insert_many([b.model_dump() for b in bands])


    users: list[User] = []

    for i in range(1, 11):
        max_bands = random.randint(0, 5)
        band_ids = random.sample(
            [b.band_id for b in bands],
            k=max_bands
        )

        user = User(
            user_id=i,
            name=f"User {i}",
            email=f"user{i}@email",
            bands=band_ids
        )

        users.append(user)

    users_col.insert_many([u.model_dump() for u in users])