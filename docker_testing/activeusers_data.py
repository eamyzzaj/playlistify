import os
import dotenv
import psycopg2
from fastapi import HTTPException, status

dotenv.load_dotenv()

# db connection setup using environment variables
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# db connection
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# function for inserting into activeusers table
def insert_active_users(num_users: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # random user ids
        user_ids_query = "SELECT user_id FROM public.Users ORDER BY RANDOM() LIMIT %s"
        cursor.execute(user_ids_query, (num_users,))
        user_ids = cursor.fetchall()

        if not user_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No users found for ActiveUsers."
            )

        active_users_data = [(user_id[0],) for user_id in user_ids]

        # bulk insert (fastest way)
        insert_sql = """
        INSERT INTO public.ActiveUsers (user_id) 
        VALUES (%s) 
        ON CONFLICT (user_id) DO NOTHING;
        """
        cursor.executemany(insert_sql, active_users_data)

        conn.commit()

        return {"message": f"Successfully inserted {len(active_users_data)} active users into ActiveUsers table."}

    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred: {str(e)}"
        )

    finally:
        # close db connection
        if conn:
            cursor.close()
            conn.close()

# Command-line argument parsing for the number of users to insert
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Insert fake active users into the ActiveUsers table.")
    parser.add_argument('num_users', type=int, help="The number of active users to insert.")
    args = parser.parse_args()

    result = insert_active_users(args.num_users)
    print(result["message"])
