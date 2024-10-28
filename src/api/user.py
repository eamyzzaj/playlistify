# user.py

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)

# user signup
# POST


# user login - ivana
# POST
@router.post("/user/login")
def user_login(username):
    with db.engine.begin() as connection:
        user = connection.execute(sqlalchemy.text("SELECT username, user_id FROM USERS WHERE username = :passeduser"), {"passeduser": username})
    if (user):
        result = connection.execute(sqlalchemy.text("INSERT INTO activeusers(user_id) VALUES (:uid)"), {"uid": user.user_id})
        return {
            "message": "Login Successful"
        }

    else:
        return {
            "message": "Login Failed"
        }

# user logout
# POST