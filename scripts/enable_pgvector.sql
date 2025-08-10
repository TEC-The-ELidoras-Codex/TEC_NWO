-- Enable pgvector & pgcrypto (for gen_random_uuid()) – both idempotent
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
