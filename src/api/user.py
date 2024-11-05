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
        

@router.get("/{user_id}/competitions", tags=["user"])
def get_user_competitions(user_id: int):
    competitions = []

    with db.engine.begin() as connection:
        # SQL query to get competitions where the user has participated
        competitions_query = sqlalchemy.text("""
            SELECT competition_id FROM usercompetitions
            WHERE user_id = :user_id AND enrollment_status = TRUE
        """)

        # Execute the query and fetch results
        result = connection.execute(competitions_query, {"user_id": user_id}).fetchall()

        # Format the response as a list of competition IDs
        competitions = [{"competition_id": row.competition_id} for row in result]

    return {"user_competitions": competitions}

@router.get("/{user_id}/all/playlists", tags=["user"])
def get_all_user_playlists(user_id: int):
    playlists = []

    with db.engine.begin() as connection:
        # SQL query to retrieve all playlists the user has submitted across competitions
        playlists_query = sqlalchemy.text("""
            SELECT p.playlist_id, p.competition_id, s.song_id, s.song_title
            FROM playlists AS p
            JOIN playlistsongs AS ps ON p.playlist_id = ps.playlist_id
            JOIN songs AS s ON ps.song_id = s.song_id
            WHERE p.user_id = :user_id
        """)

        # Execute the query and fetch results
        result = connection.execute(playlists_query, {"user_id": user_id}).fetchall()

        # Organize playlists with songs grouped under each playlist ID
        playlists_dict = {}
        for row in result:
            if row.playlist_id not in playlists_dict:
                playlists_dict[row.playlist_id] = {
                    "user_id": user_id,
                    "competition_id": row.competition_id,
                    "playlist_id": row.playlist_id,
                    "songs": []
                }
            playlists_dict[row.playlist_id]["songs"].append({
                "song_id": row.song_id,
                "song_title": row.song_title
            })

        # Convert the dictionary to a list format for the response
        playlists = list(playlists_dict.values())

    return {"user_playlists": playlists}
