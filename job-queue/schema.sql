CREATE TYPE job_status as ENUM (
    'pending',
    'processing',
    'completed',
    'failed'
);

CREATE TYPE model_name as ENUM (
    'chatgpt',
    'gemini',
    'claude'
);

CREATE TABLE jobs (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    model model_name NOT NULL DEFAULT 'chatgpt',
    input TEXT NOT NULL,
    status job_status NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    attempts SMALLINT NOT NULL DEFAULT 0 CHECK (attempts BETWEEN 0 AND 5)
);