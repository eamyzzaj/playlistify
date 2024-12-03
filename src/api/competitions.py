#competitions.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from src.api import auth

import sqlalchemy
from sqlalchemy import text

from src import database as db
from src.api import users

import json

router = APIRouter(
    prefix="/competitions",
    tags=["competitions"],
    dependencies=[Depends(auth.get_api_key)],
)


@router.get("/")
def get_competitions():
    comp_list = []
    with db.engine.begin() as connection:
        comps = connection.execute(sqlalchemy.text("SELECT competition_id, status, participants_count FROM competitions ")).fetchall()
        if not comps:
            return {"message": "No competitions found", "competitions": comp_list}
        for competition in comps:
            comp_list.append(
                {
                "competition_id": competition.competition_id,
                "status": competition.status,
                "participants": competition.participants_count
                }
            )
    return {"competitions": comp_list}


@router.post("/participants")
def join_competitions(username: str, compid: int ):
    #update the competitions table (if competition is active) to update the number of active players
    #add competition to user_competitions
    with db.engine.begin() as connection:
        get_user_id = connection.execute(sqlalchemy.text("SELECT user_id FROM users WHERE username = :passeduser"), {"passeduser": username}).scalar()


        #first check if the user is in that competition:
        is_in_comp = connection.execute(sqlalchemy.text("""
            SELECT enrollment_status
            FROM usercompetitions
            WHERE usercompetitions.user_id = :passedid 
            AND usercompetitions.competition_id = :competitionid"""), {"passedid": get_user_id, "competitionid":compid}).scalar()
        is_active = connection.execute(sqlalchemy.text("""
            SELECT status
            FROM competitions
            WHERE competition_id = :competitionid"""), {"competitionid": compid}).scalar()
        
        if is_in_comp is None:
            raise HTTPException(status_code = 404, detail = "competition not found")
        
        if is_in_comp:
            raise HTTPException(status_code = 400, detail = "already enrolled in competition")
        
        if is_active == "completed":
            raise HTTPException(status_code = 404, detail = "competition has already concluded")
            
        join_comp = connection.execute(sqlalchemy.text("""UPDATE competitions SET participants_count = participants_count + 1
                                                        WHERE competition_id = :competitionid """), {"competitionid": compid})
        add_to_user = connection.execute(sqlalchemy.text("""INSERT INTO usercompetitions(user_id, competition_id, enrollment_status, submission_status) 
                                                         VALUES(:uid, :cid, TRUE, FALSE) """),
                                                         {"uid": get_user_id, "cid":compid})
        return {
            "message": "OK"
        }
    

@router.post("/{competition_id}/votes")
def vote_on_playlist(competition_id: int, playlist_id: int, voter_user_id: int, vote: int):
    """
    Vote on a specific playlist in a competition
    Votes are integers: 1-5
    """

    if vote not in [1, 2, 3, 4, 5]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not a valid vote')

    vote_info = {
        "voter_id": voter_user_id,
        "playlist_id": playlist_id,
        "vote_score": vote
    }

    voter_exists_sql = sqlalchemy.text("""
        SELECT 1
        FROM activeusers
        WHERE user_id = :user_id
    """)

    # check if the playlist exists
    playlist_exists_sql = sqlalchemy.text("""
        SELECT competition_id
        FROM playlists
        WHERE playlist_id = :playlist_id
    """)

    # check if the user has already voted on this playlist
    vote_exists_sql = sqlalchemy.text("""
        SELECT 1
        FROM votes
        WHERE voter_user_id = :voter_id AND playlist_id = :playlist_id
    """)

    # check if all other users have submitted their playlists
    all_others_submitted_sql = sqlalchemy.text("""
        SELECT COUNT(*) AS not_submitted_count
        FROM usercompetitions
        WHERE competition_id = :competition_id AND user_id != :voter_id AND submission_status = FALSE
    """)

    # insert the vote
    insert_vote_sql = sqlalchemy.text("""
        INSERT INTO votes (voter_user_id, playlist_id, vote_score)
        VALUES (:voter_id, :playlist_id, :vote_score)
    """)

    # increment total votes for the playlist
    increment_total_votes_sql = sqlalchemy.text("""
        UPDATE playlists
        SET total_votes = total_votes + 1
        WHERE playlist_id = :playlist_id
    """)

    # query to calculate the average score if total votes match participant count
    update_average_score_sql = sqlalchemy.text("""
        WITH participant_count AS (
            SELECT COUNT(*) AS participant_count
            FROM usercompetitions
            WHERE competition_id = :competition_id AND enrollment_status = TRUE
        )
        UPDATE playlists
        SET average_score = COALESCE((
            SELECT AVG(vote_score)
            FROM votes
            WHERE votes.playlist_id = playlists.playlist_id
        ), 0)
        WHERE playlist_id = :playlist_id AND (
            SELECT total_votes FROM playlists WHERE playlist_id = :playlist_id
        ) = (
            SELECT participant_count FROM participant_count
        )
    """)

    # query to check if competition can be marked as completed
    check_and_update_competition_sql = sqlalchemy.text("""
        WITH vote_counts AS (
            SELECT playlist_id, COUNT(*) AS vote_count
            FROM votes
            WHERE playlist_id IN (SELECT playlist_id FROM playlists WHERE competition_id = :competition_id)
            GROUP BY playlist_id
        ),
        participant_count AS (
            SELECT COUNT(*) AS participant_count
            FROM usercompetitions
            WHERE competition_id = :competition_id AND enrollment_status = TRUE
        ),
        winning_playlist AS (
            SELECT playlist_id
            FROM playlists
            WHERE competition_id = :competition_id
            ORDER BY average_score DESC
            LIMIT 1
        )
        UPDATE competitions
        SET status = 'completed',
            end_time = CURRENT_TIMESTAMP,
            winner_playlist_id = (SELECT playlist_id FROM winning_playlist)
        WHERE competition_id = :competition_id AND (
            SELECT COUNT(*)
            FROM vote_counts vc, participant_count pc
            WHERE vc.vote_count = pc.participant_count
        ) = (
            SELECT COUNT(*) FROM playlists WHERE competition_id = :competition_id
        )
    """)

    # query to update average score for all playlists in a completed competition
    update_all_average_scores_sql = sqlalchemy.text("""
        UPDATE playlists
        SET average_score = COALESCE((
            SELECT AVG(vote_score)
            FROM votes
            WHERE votes.playlist_id = playlists.playlist_id
        ), 0)
        WHERE competition_id = :competition_id
    """)

    try:
        with db.engine.begin() as connection:
            # check if user exists and is active
            active_user_result = connection.execute(voter_exists_sql, {"user_id": voter_user_id}).fetchone()
            if not active_user_result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Active user not found')
            
            # check if playlist exists
            result = connection.execute(playlist_exists_sql, {"playlist_id": playlist_id}).fetchone()
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Playlist not found')

            # check if the user has already voted on this playlist
            vote_result = connection.execute(vote_exists_sql, {
                "voter_id": voter_user_id,
                "playlist_id": playlist_id
            }).fetchone()
            if vote_result:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User has already voted on this playlist')

            # check if all other users have submitted their playlists
            not_submitted_count = connection.execute(all_others_submitted_sql, {
                "competition_id": competition_id,
                "voter_id": voter_user_id
            }).scalar()
            if not_submitted_count > 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not all other users have submitted their playlists')

            # insert the vote
            connection.execute(insert_vote_sql, vote_info)

            # increment total votes for the playlist
            connection.execute(increment_total_votes_sql, {
                "playlist_id": playlist_id
            })

            # update average score for the playlist if total votes match participant count
            connection.execute(update_average_score_sql, {
                "playlist_id": playlist_id,
                "competition_id": competition_id
            })

            # update competition status if all votes are in
            connection.execute(check_and_update_competition_sql, {
                "competition_id": competition_id
            })

            # ff competition is completed, update average scores for all playlists
            connection.execute(update_all_average_scores_sql, {
                "competition_id": competition_id
            })

    except sqlalchemy.exc.SQLAlchemyError as e:
        print(f"Error with client trying to vote: \n{e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Vote unsuccessful due to server error')
    
    return {"message": "Vote successful"}



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

    comp_exists_sql = sqlalchemy.text("""
                                    SELECT 1
                                    FROM competitions
                                    WHERE competition_id = :competition_id
                                        """)

    comp_status_sql = sqlalchemy.text("""
                                    SELECT status
                                    FROM competitions
                                    WHERE competitions.competition_id = :competition_id
                                    """)
    
    comp_details_sql = sqlalchemy.text("""
                                    SELECT winner_playlist_id, 
                                            status,
                                            participants_count,
                                            users.username AS username,
                                            playlists.average_score AS avg_score,
                                            CASE
                                                WHEN end_time IS NOT NULL THEN age(end_time, start_time)
                                                ELSE '00:00:00'::interval
                                            END AS comp_length
                                    FROM competitions
                                    LEFT JOIN playlists ON playlists.playlist_id = winner_playlist_id
                                    LEFT JOIN users ON users.user_id = playlists.user_id
                                    WHERE competitions.competition_id = :competition_id
                                        """) 
    
    try:
        with db.engine.begin() as connection:
            comp_exists = connection.execute(comp_exists_sql,  {"competition_id": comp_id}).fetchone()
            
            if not comp_exists:
                raise HTTPException(status_code=404, detail="Competition not found")
            
        with db.engine.begin() as connection:
            comp_status = connection.execute(comp_status_sql, {"competition_id": comp_id}).fetchone() 
            comp_results = connection.execute(comp_details_sql, {"competition_id": comp_id}).fetchone()

        if comp_status == ('active',):
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
            overall_comp_status['winner_playlist_id'] = winner_playlist
            overall_comp_status['winner_username'] = winner_username        
        
        overall_comp_status['message'] = comp_message

        # for console logging
        if overall_comp_status['message']:
            print(f"Comp status GET results message:\n")
            formatted = overall_comp_status['message'].replace('\\n', '\n')
            print(f"{formatted}")

        return overall_comp_status

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error with client retrieving competition status: \n{e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving competition status")



class SongRequest(BaseModel):
    user_id: int
    song_id: int
    song_title: str
    artist: str


@router.post("/{competition_id}/playlists/songs")
def add_song_to_playlist(competition_id: int, song_request: SongRequest):
    song_id = song_request.song_id
    song_title = song_request.song_title
    artist = song_request.artist
    user_id = song_request.user_id

    if song_id is None or song_title is None or artist is None or user_id is None:
        raise HTTPException(status_code = 400, detail = 'incomplete request')
    
    with db.engine.begin() as connection:
        # check if the competition exists and is active, user enrollment, and user's playlist
        query = text("""
            SELECT c.status AS competition_status, uc.enrollment_status, p.playlist_id
            FROM competitions c
            LEFT JOIN usercompetitions uc ON uc.competition_id = c.competition_id AND uc.user_id = :user_id
            LEFT JOIN playlists p ON p.competition_id = c.competition_id AND p.user_id = :user_id
            WHERE c.competition_id = :competition_id
        """)
        result = connection.execute(query, {"competition_id": competition_id, "user_id": user_id}).fetchone()

        if not result or result.competition_status != 'active':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Competition not active or not found")
        
        if not result.enrollment_status:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not enrolled in the competition")

        playlist_id = result.playlist_id

        # if the user doesn't have a playlist, create a new one
        if not playlist_id:
            create_playlist_sql = text("""
                INSERT INTO playlists (user_id, competition_id)
                VALUES (:user_id, :competition_id)
                RETURNING playlist_id
            """)
            playlist_id = connection.execute(create_playlist_sql, {"user_id": user_id, "competition_id": competition_id}).scalar()

            # update the usercompetitions table with the new playlist_id
            update_user_comp_sql = text("""
                UPDATE usercompetitions
                SET playlist_id = :playlist_id
                WHERE user_id = :user_id AND competition_id = :competition_id
            """)
            connection.execute(update_user_comp_sql, {"playlist_id": playlist_id, "user_id": user_id, "competition_id": competition_id})

        # check if the song exists, if not insert it
        song_exists_sql = text("""
            INSERT INTO songs (song_id, song_title, artist)
            VALUES (:song_id, :song_title, :artist)
            ON CONFLICT (song_id) DO NOTHING
        """)
        connection.execute(song_exists_sql, {"song_id": song_id, "song_title": song_title, "artist": artist})


        # check if the song is already in the user's playlist
        song_in_playlist_sql = text("""
            SELECT id FROM playlistsongs
            WHERE playlist_id = :playlist_id AND song_id = :song_id
        """)
        song_in_playlist = connection.execute(song_in_playlist_sql, {"playlist_id": playlist_id, "song_id": song_id}).fetchone()
            
        if song_in_playlist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Song already in playlist")

        # determine the song_order
        song_order_sql = text("""
            SELECT COUNT(*) FROM playlistsongs
            WHERE playlist_id = :playlist_id
        """)
        song_order = connection.execute(song_order_sql, {"playlist_id": playlist_id}).scalar() + 1

        # add the song to the PlaylistSongs table
        add_song_to_playlist_sql = text("""
            INSERT INTO playlistsongs (playlist_id, song_id, song_order)
            VALUES (:playlist_id, :song_id, :song_order)
        """)
        connection.execute(add_song_to_playlist_sql, {"playlist_id": playlist_id, "song_id": song_id, "song_order": song_order})

    response = {
        "message": "Song successfully added to playlist",
        "playlist_status": True,
        "song_details": {
            "song_id": song_id,
            "song_title": song_title,
            "artist": artist
        }
    }

    return response


class SubmitPlaylistRequest(BaseModel):
    user_id: int
    playlist_id: int



@router.post("/{competition_id}/submit")
def submit_playlist(competition_id: int, request_body: SubmitPlaylistRequest):
    user_id = request_body.user_id
    playlist_id = request_body.playlist_id
    
    with db.engine.begin() as connection:
        # checks for competition status, user enrollment, and playlist ownership
        query = text("""
            SELECT c.status AS competition_status,
                   uc.enrollment_status,
                   uc.submission_status,
                   p.user_id AS playlist_owner_id
            FROM competitions c
            JOIN usercompetitions uc ON uc.competition_id = c.competition_id AND uc.user_id = :user_id
            JOIN playlists p ON p.playlist_id = :playlist_id
            WHERE c.competition_id = :competition_id AND p.competition_id = :competition_id
        """)
        result = connection.execute(query, {
            "competition_id": competition_id,
            "user_id": user_id,
            "playlist_id": playlist_id
        }).fetchone()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Competition or playlist not found")

        if result.competition_status != 'active':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Competition is not active")

        if not result.enrollment_status:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not enrolled in the competition")

        if result.submission_status:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Playlist already submitted")

        if result.playlist_owner_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not own the playlist")

        # update submission_status in usercompetitions table
        update_submission_sql = text("""
            UPDATE usercompetitions
            SET submission_status = TRUE
            WHERE user_id = :user_id AND competition_id = :competition_id
        """)

        connection.execute(update_submission_sql, {
            "user_id": user_id,
            "competition_id": competition_id
        })


    response = {
        "message": "Playlist submission successful",
        "submission_status": True
    }
    return response
