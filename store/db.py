# db.py
# Database connection helper shared by both ingest/ and retrieve/ subpackages

import os
from pathlib import Path
import psycopg
from pgvector.psycopg import register_vector

SCHEMA = Path(__file__).parent / "schema.sql"

def get_connection():
    conn = psycopg.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=os.environ.get("POSTGRES_PORT", 5432),
        user=os.environ("POSTGRES_USER"),
        password=os.environ("POSTGRES_PASSWORD"),
        dbname=os.environ("POSTGRES_DB")
    )
    conn.execute(SCHEMA.read_text())
    conn.commit()
    register_vector(conn) # magic from pgvector library
    return conn