import os
import dotenv
import psycopg2
import random
import sys

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

    def insert_playlist_songs(num_entries):
        try:
            # exisintg playlists
            cursor.execute("SELECT playlist_id FROM Playlists;")
            playlists = cursor.fetchall()

            # songs in db
            cursor.execute("SELECT song_id FROM Songs;")
            songs = cursor.fetchall()

            if not playlists or not songs:
                print("No playlists or songs found to link.")
                return

            playlist_songs_data = []

            for playlist in playlists:
                playlist_id = playlist[0]
                #about 5 random songs from existing 
                selected_songs = random.sample(songs, min(len(songs), 5)) 

                for order, song in enumerate(selected_songs, start=1):
                    song_id = song[0]
                    playlist_songs_data.append((playlist_id, song_id, order))

            if playlist_songs_data:
                cursor.executemany("""
                    INSERT INTO PlaylistSongs (playlist_id, song_id, song_order)
                    VALUES (%s, %s, %s);
                """, playlist_songs_data)
                conn.commit()
                print(f"Inserted {len(playlist_songs_data)} records into PlaylistSongs table.")

            else:
                print("No new data to insert.")

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
            insert_playlist_songs(num_entries)
        except ValueError:
            print("Please provide a valid number.")

except Exception as e:
    print(f"Failed to connect to the database: {e}")
