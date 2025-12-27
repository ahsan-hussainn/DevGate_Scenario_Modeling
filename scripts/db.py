import os
import psycopg2


def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST_SUPABASE"),
        database=os.getenv("DB_NAME_SUPABASE"),
        user=os.getenv("DB_USER_SUPABASE"),
        password=os.getenv("DB_PASSWORD_SUPABASE"),
        port=os.getenv("DB_PORT_SUPABASE", 5432)
    )
    return conn