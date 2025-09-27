
-- Run this SQL against Postgres to create tables (or use Alembic autogenerate)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    filename VARCHAR(512) NOT NULL,
    path VARCHAR(1024) NOT NULL,
    s3_key VARCHAR(1024),
    uploaded_at TIMESTAMP DEFAULT now()
);

DO $$ BEGIN
    CREATE TYPE IF NOT EXISTS jobstatus AS ENUM ('pending','processing','done','failed');
EXCEPTION WHEN duplicate_object THEN null; END $$;

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    celery_id VARCHAR(255),
    status jobstatus DEFAULT 'pending',
    input_asset_id INTEGER REFERENCES assets(id),
    output_path VARCHAR(1024),
    output_s3_key VARCHAR(1024),
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS analytics (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    event_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT now()
);
