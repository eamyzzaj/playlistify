#competitions.py
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from src import database as db

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