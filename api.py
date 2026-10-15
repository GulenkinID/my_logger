from fastapi import FastAPI
import psycopg2
from config import DB_CONFIG


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Log Analyzer API is running"}


@app.get("/logs")
def get_logs():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, log_date, log_level, message FROM logs")
            rows = cursor.fetchall()
            
            
    return [
        {"id": row[0], "log_date": row[1], "log_level": row[2], "message": row[3]} 
        for row in rows
    ]