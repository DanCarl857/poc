from app.db import get_conn, init_db

init_db()

conn = get_conn()

conn.execute("""
INSERT OR IGNORE INTO clinics (clinic_key, name, daily_question_limit, daily_token_limit)
VALUES (?, ?, ?, ?)
""", ("ffltest", "Free for Life Group", 50, 50000))

conn.commit()
conn.close()

print("Clinic seeded")