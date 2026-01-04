from fastapi import FastAPI
from pydantic import BaseModel
from persistence import User,create_user, add_band, band_listeners

app = FastAPI()

@app.post('/create')
async def create_user_endpoint(user:User):
    result = await create_user(user)
    return {"message": "User created successfully", "user_id": user.user_id}

class AddBandRequest(BaseModel):
    user_id: int
    band: str
@app.post('/add-band')
async def add_band_endpoint(query: AddBandRequest):
    result = await add_band(user_id=query.user_id, band=query.band)
    return {"Added_Band": query.band}


@app.get('/band-listeners')
async def band_listeners_endpoint():
    return await band_listeners()