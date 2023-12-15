
from typing import Union, List, Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter

from . import router
import lib




@router.post("/users/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = lib.helper.auth_helper.fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = lib.helper.auth_helper.UserInDB(**user_dict)
    hashed_password = lib.helper.auth_helper.fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[lib.helper.auth_helper.User, Depends(lib.helper.auth_helper.get_current_active_user)]
):
    return current_user


