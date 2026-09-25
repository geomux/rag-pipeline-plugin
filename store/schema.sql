-- schema.sql
-- Schema for the vector database (paraphrased per https://github.com/pgvector/pgvector)

create extension if not exists vector;

create table if not exists doc_chunks (
    id bigserial primary key,
    source_path text not null,
    chunk_index int not null,
    content text not null,
    embedding vector(768),
    metadata jsonb default '{}',
    created_at timestamptz default now(),
    unique (source_path, chunk_index)
);

create index if not exists doc_chunks_embedding_idx on doc_chunks using hnsw (embedding vector_cosine_ops);