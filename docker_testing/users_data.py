import os
import dotenv
import argparse
import psycopg2
import psycopg2.extras
from faker import Faker

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

    fake = Faker()

    def insert_users(count):
        try:
            data = []
            existing_usernames = set() # tracks usernames
            duplicates = 0

            for _ in range(count):  
                username = fake.user_name()
                name = fake.name()

                # want to only insert UNIQUE usernames 
                if username not in existing_usernames:
                    existing_usernames.add(username)
                    data.append((username, name))
                else:
                    duplicates += 1  # keeping track of how many were not inserted

            if data:
                insert_query = """
                    INSERT INTO public.Users (username, name)
                    VALUES %s
                    ON CONFLICT (username) DO NOTHING
                """
                cursor.execute("BEGIN;")
                psycopg2.extras.execute_values(cursor, insert_query, data)
                conn.commit()

                print(f"Successfully inserted {len(data)} fake users into Users table.")
                print(f"Skipped {duplicates} duplicate users due to conflict.")
            else:
                print("No new users to insert.")

        except Exception as e:
            conn.rollback()
            print(f"Error occurred: {e}")

        finally:
            cursor.close()
            conn.close()

    if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Insert fake users into the Users table.")
        parser.add_argument('count', type=int, help="Number of users to generate and insert.")
        args = parser.parse_args()

        insert_users(args.count)

except Exception as e:
    print(f"Failed to connect to the database: {e}")
