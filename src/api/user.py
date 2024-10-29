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
class userCreateRequest(BaseModel):
    username: str
    name: str

@router.post("/signup")
def create_user(user: userCreateRequest):

    new_user = {
                    "username": user.username,
                    "name": user.name
                }
    
    user_insert_sql = sqlalchemy.text("""
                        INSERT INTO users (username, name)
                        VALUES (:username, :name)
                        RETURNING user_id
                        """)
    try:
        with db.engine.begin() as connection:
            newuser_id = connection.execute(user_insert_sql, new_user).scalar()
        return {"message": 'Account created successfully', "user_id": newuser_id}
    except Exception as e:
        print(f"Account creation failed: {e}")
        return {"message": 'Account creation failed', "user_id": None}
    
    

# user login - ivana
# POST
@router.post("/login")
def user_login(username):
    with db.engine.begin() as connection:
        user = connection.execute(sqlalchemy.text("SELECT username, user_id FROM USERS WHERE username = :passeduser"), {"passeduser": username}).fetchone()
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
@router.post("/logout")
def user_logout(username: str):
    # Check if the user is in the activeusers table
    with db.engine.begin() as connection:
        active_user = connection.execute(
            sqlalchemy.text("SELECT user_id FROM activeusers WHERE user_id = (SELECT user_id FROM USERS WHERE username = :passeduser)"),
            {"passeduser": username}
        ).fetchone()

        # If user is found in activeusers, proceed to log them out
        if active_user:
            # Remove the user from activeusers table to log them out
            connection.execute(
                sqlalchemy.text("DELETE FROM activeusers WHERE user_id = :uid"),
                {"uid": active_user.user_id}
            )
            return {"message": "Logout successful"}
        else:
            return {"message": "Logout failed - user not logged in"}
        