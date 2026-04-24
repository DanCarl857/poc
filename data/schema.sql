CREATE TABLE IF NOT EXISTS clinics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clinic_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    daily_question_limit INTEGER NOT NULL DEFAULT 100,
    daily_token_limit INTEGER NOT NULL DEFAULT 100000,
    is_active INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS clinic_daily_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clinic_id INTEGER NOT NULL,
    usage_date TEXT NOT NULL,
    questions_used INTEGER NOT NULL DEFAULT 0,
    tokens_used INTEGER NOT NULL DEFAULT 0,
    UNIQUE(clinic_id, usage_date),
    FOREIGN KEY(clinic_id) REFERENCES clinics(id)
);

CREATE TABLE IF NOT EXISTS chat_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clinic_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT,
    prompt_tokens INTEGER NOT NULL DEFAULT 0,
    completion_tokens INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    success INTEGER NOT NULL DEFAULT 1,
    error_message TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(clinic_id) REFERENCES clinics(id)
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chunk_id TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL,
    doc_type TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cached_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clinic_id INTEGER NOT NULL,
    question_hash TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    sources_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(clinic_id, question_hash),
    FOREIGN KEY(clinic_id) REFERENCES clinics(id)
);