import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        print("Testing Supabase connection...")
        print("Host:", os.getenv("DB_HOST"))
        print("Port:", os.getenv("DB_PORT"))

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode="require",
            connect_timeout=10
        )

        cur = conn.cursor()
        cur.execute("SELECT now();")
        print("✅ Connected successfully:", cur.fetchone())

        cur.close()
        conn.close()

    except Exception as e:
        print("❌ Connection failed:")
        print(e)

if __name__ == "__main__":
    test_connection()