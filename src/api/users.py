# user.py

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)


# user signup
# POST
class UserCreateRequest(BaseModel):
    username: str
    name: str

@router.post("/")
def create_user(user: UserCreateRequest):
    if len(user.username) > 50:
        raise HTTPException(status_code=400, detail="Username must be less than 50 characters.")
    
    if len(user.name) > 100:
        raise HTTPException(status_code=400, detail="Name must be less than 100 characters.")

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
        raise HTTPException(status_code=400, detail="Account creation failed, try a different username.")
    

# POST
@router.post("/sessions")
def user_login(username: str):
    with db.engine.begin() as connection:
        user_query = sqlalchemy.text("""
                                        SELECT u.username, u.user_id AS registered_user, a.user_id AS active_user
                                        FROM users u
                                        LEFT JOIN activeusers a
                                        ON u.user_id = a.user_id
                                        WHERE u.username = :inactive_username
                                     """)
        result = connection.execute(user_query, {"inactive_username": username}).fetchone()
        
        # validate if user exists or is already active
        if result is None or result.registered_user is None:
            # user not found in users table
            raise HTTPException(status_code=404, detail="User not found.")
        
        if result.active_user is not None:
            # user is already in activeusers table
            raise HTTPException(status_code=400, detail="User is already active.")
        
        # if user is found and not active, insert them into ActiveUsers table
        insert_query = sqlalchemy.text("""
            INSERT INTO activeusers (user_id, last_active_time)
            VALUES (:user_id, NOW())
        """)
        
        connection.execute(insert_query, {"user_id": result[1]})
        
        return {"message": "User successfully logged in and marked as active."}


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
            raise HTTPException(status_code = 404, detail = 'User not found')
        

@router.get("/{user_id}/competitions", tags=["users"])
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


@router.get("/{user_id}/all/playlists", tags=["users"])
def get_all_user_playlists(user_id: int):
    playlists = []

    with db.engine.begin() as connection:
        # SQL query to retrieve all playlists the user has ted across competitions
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


@router.get("/users/{user_id}/voting-pattern-trends")
def get_user_voting_pattern_trends(user_id: int):
    with db.engine.begin() as connection:
        query = sqlalchemy.text("""
            WITH UserExists AS (
                SELECT user_id
                FROM users
                WHERE user_id = :user_id
            ),
            VotingSummary AS (
                SELECT
                    voter_user_id,
                    COUNT(vote_id) AS total_votes_cast,
                    AVG(vote_score) AS average_score_given
                FROM votes
                WHERE voter_user_id = :user_id
                GROUP BY voter_user_id
            ),
            VotingTrend AS (
                SELECT 
                    vote_id,
                    vote_score,
                    LAG(vote_score) OVER (ORDER BY vote_time) AS previous_vote_score,
                    LEAD(vote_score) OVER (ORDER BY vote_time) AS next_vote_score,
                    voter_user_id
                FROM votes
                WHERE voter_user_id = :user_id
            )
            SELECT
                u.user_id,
                vs.total_votes_cast,
                vs.average_score_given,
                json_agg(json_build_object(
                    'vote_id', vt.vote_id,
                    'vote_score', vt.vote_score,
                    'previous_vote_score', vt.previous_vote_score,
                    'next_vote_score', vt.next_vote_score
                )) AS voting_trend_analysis
            FROM
                UserExists u
            LEFT JOIN VotingSummary vs ON u.user_id = vs.voter_user_id
            LEFT JOIN VotingTrend vt ON u.user_id = vt.voter_user_id
            GROUP BY
                u.user_id, vs.total_votes_cast, vs.average_score_given;
        """)

        result = connection.execute(query, {"user_id": user_id}).fetchone()

        # handle user does not exist
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        response_data = {
            "user_id": result.user_id,
            "total_votes_cast": result.total_votes_cast,
            "average_score_given": float(result.average_score_given),
            "voting_trend_analysis": result.voting_trend_analysis
        }

        return response_data
