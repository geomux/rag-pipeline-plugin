# cli.py
# Python module for ingesting documents, chunking, and embedding with the local embedding model

import argparse
import os
import psycopg
import sys
import tomllib
from dotenv import load_dotenv

from ingest.loader import load_docs
from ingest.chunker import chunk_doc
from ingest.embed import embed, embed_batch
from ingest.upsert import upsert_chunks
from store.db import get_connection


# !functions from the retrieve/ subpackage will import here
# from retrieve.query import

# !functions from the middleware/ subpackage will import here
# from middleware.registry import

def main():
    load_dotenv()
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    
    parser = argparse.ArgumentParser(description="RAG Pipeline CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("ingest").add_argument("path", nargs="?",default="./docs")
    sub.add_parser("retrieve").add_argument("prompt")
    sub.add_parser("serve").add_argument("harness")
    args = parser.parse_args()

    model = config["embedding"]["model"]

    if args.command == "ingest":
        try:
            conn = get_connection()
        except psycopg.OperationalError as e:
            sys.exit(f"Could not connect to Postgres database: {e}\nIs the container running? Try: docker compose up -d")
        with conn:
            for doc in load_docs(args.path):
                chunks = chunk_doc(doc, config["chunking"]["max_chars"])
                if not chunks:
                    continue # Skip documents with no valid chunks (i.e. empty files)
                texts = ["search_document: " + c.text for c in chunks]
                upsert_chunks(conn, doc.path, chunks, embed_batch(texts, model))
                print(f"{doc.path}: ingested {len(chunks)} chunks.")


    if args.command == "retrieve":
        # query vector database embeddings with user prompt logic goes here after Retrieve/ subpackage ready
        pass

    if args.command == "serve":
        # call middleware components to connect user prompt to model logic goes here after Middleware/ subpackage ready
        pass

if __name__ == "__main__":
    main()