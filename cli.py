# cli.py
# Python module for ingesting documents, chunking, and embedding with the local embedding model

import argparse
import os
import tomllib

from dotenv import load_dotenv

# !functions from the ingest/ subpackage will import here
# from ingest.loader import
# from ingest.chunker import
# from ingest.embed import
# from ingest.upsert import

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
        # ingest documents logic goes here after Ingest/ subpackage ready
        pass

    if args.command == "retrieve":
        # query vector database embeddings with user prompt logic goes here after Retrieve/ subpackage ready
        pass

    if args.command == "serve":
        # call middleware components to connect user prompt to model logic goes here after Middleware/ subpackage ready
        pass

if __name__ == "__main__":
    main()