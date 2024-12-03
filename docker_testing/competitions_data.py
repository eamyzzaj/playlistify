import os
import dotenv
import psycopg2
from faker import Faker
import random
from datetime import timedelta
import sys

# Load environment variables from the .env file
dotenv.load_dotenv()

# Database connection setup using environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# db connection
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # where fake data is coming from
    fake = Faker()

    def insert_competitions(num_competitions):
        try:
            competitions_data = []
            for _ in range(num_competitions):  # Insert specified number of competitions
                status = random.choice(['active', 'completed', 'upcoming'])

                start_time = fake.date_time_this_year()

                if status == 'completed':
                    # randome time addition so end time after start
                    end_time = start_time + timedelta(minutes=random.randint(30, 1440))  # 30 minutes to 24 hours later
                else:
                    end_time = None

                competitions_data.append((status, start_time, end_time))

            # batch insert
            if competitions_data:
                cursor.executemany("""
                    INSERT INTO public.Competitions (status, start_time, end_time)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, competitions_data)
                conn.commit()
                print(f"Successfully inserted {len(competitions_data)} fake competitions into Competitions table.")
            else:
                print("No new competitions to insert.")

        except Exception as e:
            conn.rollback()
            print(f"Error occurred: {e}")

        finally:
            cursor.close()
            conn.close()

    if len(sys.argv) != 2:
        print("Usage: python3 script_name.py <number_of_competitions>")
    else:
        try:
            num_competitions = int(sys.argv[1])
            insert_competitions(num_competitions)
        except ValueError:
            print("Please provide a valid number.")
except Exception as e:
    print(f"Failed to connect to the database: {e}")
