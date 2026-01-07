from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from persistence import User, Band, create_user, get_user, create_band, get_band

app = FastAPI()

@app.post(
    '/users', 
    status_code=status.HTTP_201_CREATED )
async def create_user_endpoint(user:User, response: Response):
    try:
        user_id = await create_user(user)
        # return {"message": "User created successfully", "user_id": user.user_id}
    except Exception:

        #TODO manage detailed exceptions

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    response.headers["Location"] = f"/users/{user_id}"
    return {"id": user_id}

@app.get(
    "/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK)
async def get_user_endpoint(user_id: int):

    user = await get_user(user_id)
    if user is None:
        raise HTTPException(404, "User not found")
    return user

@app.post(
    '/bands',
    status_code=status.HTTP_201_CREATED 
    )
async def add_band_endpoint(band:Band, response: Response):
    try:
        band_id = await create_band(band=band)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    response.headers["Location"] = f"/bands/{band_id}"
    return {"id": band_id}

@app.get(
    '/bands/{band_id}',
    response_model=Band,
    status_code=status.HTTP_200_OK)
async def get_band_endpoint(band_id: int):

    band = await get_band(band_id)

    if band is None:
        raise HTTPException(404, "Band not found")
        
    return band