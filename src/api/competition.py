#competitions.py
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db
from src.api import user

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