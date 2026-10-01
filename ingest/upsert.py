# upsert.py
# Updates and/or inserts all chunks from a document into the doc_chunks postgres table

from pgvector import Vector
from psycopg import Connection

from ingest.chunker import Chunk

def upsert_chunks(conn: Connection, source_path: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
    """Replace all stored chunks for source_path with the passed in chunks and vectors in one process."""
    with conn.cursor() as cur:
        cur.execute("delete from doc_chunks where source_path = %s", (source_path,))
        cur.executemany(
            "INSERT INTO doc_chunks (source_path, chunk_index, content, embedding) "
            "values (%s, %s, %s, %s)",
            [(source_path, c.index, c.text, Vector(v)) for c, v in zip(chunks, vectors)],
        )
    conn.commit()