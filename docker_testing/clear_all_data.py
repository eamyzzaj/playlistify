import os
import dotenv
import psycopg2
from fastapi import HTTPException, status

dotenv.load_dotenv()

# db connection
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# db connection setup
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    try:
        cursor.execute("""
            TRUNCATE TABLE 
                ActiveUsers,
                Votes,
                UserCompetitions,
                PlaylistSongs,
                Playlists,
                Songs,
                Competitions,
                Users
            RESTART IDENTITY CASCADE;
        """)
        conn.commit()
        print("All tables truncated and sequences reset.")
    except Exception as e:
        conn.rollback()
        print(f"Error occurred while truncating tables: {e}")
    finally:
        cursor.close()
        conn.close()

except Exception as e:
    print(f"Failed to connect to the database: {e}")
