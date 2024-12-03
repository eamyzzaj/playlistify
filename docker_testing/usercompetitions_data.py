import os
import dotenv
import psycopg2
import random
import argparse

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

    def insert_usercompetitions(num_entries):
        try:
            user_competitions_data = []

            # existing users
            cursor.execute("SELECT user_id FROM public.Users")
            existing_users = cursor.fetchall()

            # existing comps that are not 'upcoming'
            cursor.execute("""
                SELECT competition_id 
                FROM public.Competitions
                WHERE status IN ('active', 'completed')
            """)
            existing_competitions = cursor.fetchall()

            if not existing_users:
                print("No existing users found.")
                return

            if not existing_competitions:
                print("No active or completed competitions found.")
                return

            for _ in range(num_entries):  
                # picks randomly from existing users and active and completed comps
                user_id = random.choice(existing_users)[0]  
                competition_id = random.choice(existing_competitions)[0]  
                
                user_competitions_data.append((user_id, competition_id))

            if user_competitions_data:
                cursor.executemany("""
                    INSERT INTO public.UserCompetitions (user_id, competition_id)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id, competition_id) DO NOTHING;
                """, user_competitions_data)
                conn.commit()
                print(f"Successfully inserted {len(user_competitions_data)} user-competition entries into UserCompetitions table.")
            else:
                print("No new user-competition data to insert.")

        except Exception as e:
            conn.rollback()
            print(f"Error occurred: {e}")

        finally:
            cursor.close()
            conn.close()

    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Insert user-competition pairs into the database.")
        parser.add_argument('num_entries', type=int, help="Number of user-competition pairs to insert.")
        args = parser.parse_args()

        insert_usercompetitions(args.num_entries)

except Exception as e:
    print(f"Failed to connect to the database: {e}")
