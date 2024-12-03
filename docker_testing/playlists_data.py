import os
import dotenv
import psycopg2
import random
import argparse
from faker import Faker

dotenv.load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


try:
    # db connect
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    fake = Faker()

    def insert_fake_playlists(num_entries):
        try:
            conn.autocommit = False

            # existing users
            cursor.execute("SELECT user_id FROM public.Users;")
            existing_users = [row[0] for row in cursor.fetchall()]

            # existing active/completed competitions
            cursor.execute("""
                SELECT competition_id 
                FROM public.Competitions 
                WHERE status IN ('active', 'completed');
            """)
            valid_competitions = [row[0] for row in cursor.fetchall()]

            if not existing_users:
                print("No existing users found. Please add users first.")
                return

            if not valid_competitions:
                print("No active or completed competitions found. Please add active/completed competitions.")
                return

        
            playlists_data = []
            # will pull from existing data
            for _ in range(num_entries): 
                user_id = random.choice(existing_users)  
                competition_id = random.choice(valid_competitions)  

                # trying to avoid conflicst
                cursor.execute("""
                    SELECT 1 FROM public.Playlists
                    WHERE user_id = %s AND competition_id = %s;
                """, (user_id, competition_id))

                if cursor.fetchone() is None:
                    playlists_data.append((user_id, competition_id))

            # bulk insert!!
            if playlists_data:
                cursor.executemany("""
                    INSERT INTO public.Playlists (user_id, competition_id)
                    VALUES (%s, %s)
                """, playlists_data)
                conn.commit()
                print(f"Successfully inserted {len(playlists_data)} fake playlists linked to active and completed competitions.")
            else:
                print("No new playlists to insert.")

        except Exception as e:
            conn.rollback()
            print(f"Error occurred: {e}")

        finally:
            cursor.close()
            conn.close()

    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Insert fake playlists linked to active/completed competitions.")
        parser.add_argument('num_entries', type=int, help="Number of playlists to insert.")
        args = parser.parse_args()

        insert_fake_playlists(args.num_entries)

except Exception as e:
    print(f"Failed to connect to the database: {e}")
