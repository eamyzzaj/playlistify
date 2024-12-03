import os
import sys
import dotenv
import psycopg2
import random

dotenv.load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    def insert_votes(num_entries):
        try:
            # existing users
            cursor.execute("SELECT user_id FROM Users;")
            users = cursor.fetchall()

            # existing playlists
            cursor.execute("SELECT playlist_id FROM Playlists;")
            playlists = cursor.fetchall()

            if not users or not playlists:
                print("No users or playlists found for voting.")
                return

            votes_data = []
            inserted_count = 0     

            for _ in range(num_entries):
                voter_user = random.choice(users)[0]
                playlist = random.choice(playlists)[0]

                # no duplicate votes
                cursor.execute("""
                    SELECT 1 FROM Votes WHERE voter_user_id = %s AND playlist_id = %s;
                """, (voter_user, playlist))

                if cursor.fetchone() is None:  
                    vote_score = random.choice([1, 2, 3, 4, 5])
                    votes_data.append((voter_user, playlist, vote_score))
                    inserted_count += 1

            if votes_data:
                cursor.executemany("""
                    INSERT INTO Votes (voter_user_id, playlist_id, vote_score)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, votes_data)
                conn.commit()
                print(f"Successfully inserted {inserted_count} votes into the Votes table.")

            else:
                print("No new votes to insert.")

        except Exception as e:
            conn.rollback()
            print(f"Error occurred: {e}")

        finally:
            cursor.close()
            conn.close()

    if len(sys.argv) != 2:
        print("Usage: python3 script_name.py <number_of_entries>")
    else:
        try:
            num_entries = int(sys.argv[1])
            insert_votes(num_entries)
        except ValueError:
            print("Please provide a valid number.")

except Exception as e:
    print(f"Failed to connect to the database: {e}")
