#competitions.py
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db
from src.api import user

import json

router = APIRouter(
    prefix="/competition",
    tags=["competition"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("/")
def get_competitions():
    comp_list = []
    with db.engine.begin() as connection:
        comps = connection.execute(sqlalchemy.text("SELECT competition_id, status, participants_count FROM competitions ")).fetchall()
        for competition in comps:
            comp_list.append(
                {
                "competition_id": competition.competition_id,
                "status": competition.status,
                "participants": competition.participants_count
                }
            )
    return comp_list

@router.post("/join")
def join_competitions(username: str, compid: int ):
    #update the competitions table (if competition is active) to update the number of active players
    #add competition to user_competitions
    with db.engine.begin() as connection:
        get_user_id = connection.execute(sqlalchemy.text("SELECT user_id FROM users WHERE username = :passeduser"), {"passeduser": username}).scalar()
        join_comp = connection.execute(sqlalchemy.text("""UPDATE competitions SET participants_count = participants_count + 1
                                                        WHERE competition_id = :competitionid """), {"competitionid": compid})
        add_to_user = connection.execute(sqlalchemy.text("""INSERT INTO usercompetitions(user_id, competition_id, enrollment_status, submission_status) 
                                                         VALUES(:uid, :cid, TRUE, FALSE) """),
                                                         {"uid": get_user_id, "cid":compid})
        return {
            "message": "OK"
        }
    
@router.post("/{competition_id}/vote")
def vote_on_playlist(competition_id: int, playlist_id: int, voter_user_id: int, vote: int):
    """
    Vote on a specific playlist in a competition\n
    Votes are integers: 1-5
    """

    vote_info = {
        "voter_id": voter_user_id,
        "playlist_id": playlist_id,
        "vote_score": vote
    }

    insert_vote_sql = sqlalchemy.text("""
                                    INSERT INTO votes (voter_user_id, playlist_id, vote_score)
                                    VALUES (:voter_id, :playlist_id, :vote_score)
                                        """)
    
    try:
        with db.engine.begin() as connection:
            connection.execute(insert_vote_sql, vote_info)
    except Exception as e:
        print(f"Error trying to vote: {e}")
        return "Vote unsuccessful"
    return "OK"

@router.get("/{competition_id}/status")
def get_competition_status(comp_id: int):
    """
    Get status of specific competition\n
    Returns winner's playlist id, username, and message about comp outcome
    """
    overall_comp_status = {
        "winner_playlist_id": None,
        "winner_username": None,
        "message": None
    }

    comp_status_sql = sqlalchemy.text("""
                                    SELECT winner_playlist_id, 
                                            status,
                                            participants_count,
                                            users.username AS username,
                                            playlists.average_score AS avg_score,
                                            age(end_time, start_time) AS comp_length
                                    FROM competitions
                                    LEFT JOIN playlists ON playlists.playlist_id = winner_playlist_id
                                    LEFT JOIN users ON users.user_id = playlists.user_id
                                    WHERE competitions.competition_id = :competition_id
                                        """)
    
    try:
        with db.engine.begin() as connection:
            comp_results = connection.execute(comp_status_sql, {"competition_id": comp_id}).fetchone()

        comp_status = comp_results.status

        if comp_status == 'active':
            comp_message = "Competition is still in progress - check again later!"
        else:
            winner_playlist = comp_results.winner_playlist_id
            winner_username = comp_results.username
            playlist_score = comp_results.avg_score
            num_players = comp_results.participants_count
            comp_length = int((comp_results.comp_length).total_seconds()) #get comp length in total seconds
            comp_length = comp_length//60 #get comp length converted to minutes (rounded down)
            comp_message = f"Competition is {comp_status}.\\n" \
                                f"User {winner_username} won with a score of {playlist_score} on their playlist!\\n" \
                                f"Total participants: {num_players}\\n" \
                                f"Competition length: {comp_length} minutes"
            
        overall_comp_status['message'] = comp_message

    except Exception as e:
        print(f"Error retreving competition's status: {e}")
        return "Competition not found"

    # for console logging
    if overall_comp_status['message']:
        print(f"Comp status GET results message:\n")
        formatted = overall_comp_status['message'].replace('\\n', '\n')
        print(f"{formatted}")

    return overall_comp_status