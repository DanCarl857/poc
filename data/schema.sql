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
    created_at TEXT NOT NULL,
    FOREIGN KEY(clinic_id) REFERENCES clinics(id)
);