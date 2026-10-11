import os
import pymysql
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "rootpassword")
DB_NAME = os.getenv("DB_NAME", "research_portal")


# connect to mysql
def get_db_connection(database=None):
    db_target = database if database is not None else DB_NAME
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=db_target,
        cursorclass=DictCursor,
        autocommit=True,
        charset="utf8mb4"
    )


# check if mysql is reachable
def check_db_connection():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 AS ping;")
            result = cursor.fetchone()
        conn.close()
        return result is not None and result.get("ping") == 1
    except Exception as exc:
        print(f"Database health check error: {exc}")
        return False


# create database and table if not created already
def init_db(schema_path=None):
    conn = get_db_connection(database="")
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cursor.execute(f"USE `{DB_NAME}`;")
            
            cursor.execute("""
                SELECT COUNT(*) AS cnt 
                FROM information_schema.tables 
                WHERE table_schema = %s AND table_name = 'opportunities';
            """, (DB_NAME,))
            table_exists = cursor.fetchone()["cnt"] > 0
            
            if not table_exists:
                if schema_path is None:
                    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    schema_path = os.path.join(base_dir, "database", "schema.sql")
                
                with open(schema_path, "r", encoding="utf-8") as f:
                    sql_script = f.read()
                
                statements = [stmt.strip() for stmt in sql_script.split(";") if stmt.strip()]
                for statement in statements:
                    cursor.execute(statement)
                print("Database table initialized successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    print(f"Connecting to database at {DB_HOST}:{DB_PORT}...")
    init_db()
    if check_db_connection():
        print("Database connection verified.")
    else:
        print("Database connection failed.")
