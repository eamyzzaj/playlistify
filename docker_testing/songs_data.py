import os
import dotenv
import psycopg2
from faker import Faker
import sys

dotenv.load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Database connection details
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

    def insert_songs(num_songs):
        try:
            songs_data = []

            for _ in range(num_songs):  
                song_title = fake.sentence(nb_words=3)
                artist = fake.name()
                songs_data.append((song_title, artist))

            if songs_data:
                cursor.executemany("""
                    INSERT INTO public.Songs (song_title, artist)
                    VALUES (%s, %s);
                """, songs_data)
                conn.commit()
                print(f"Fake data inserted into Songs table successfully! Inserted {num_songs} songs.")

            else:
                print("No new songs to insert.")

        except Exception as e:
            conn.rollback()
            print(f"Error occurred: {e}")

        finally:
            cursor.close()
            conn.close()

    if len(sys.argv) != 2:
        print("Usage: python3 script_name.py <number_of_songs>")
    else:
        try:
            num_songs = int(sys.argv[1])
            insert_songs(num_songs)
        except ValueError:
            print("Please provide a valid number.")

except Exception as e:
    print(f"Failed to connect to the database: {e}")
