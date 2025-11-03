import sqlite3
from datetime import datetime

DB_NAME = "habits.db"

def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def create_table():
    """Create the habits table if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            habit TEXT NOT NULL,
            frequency TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_done TIMESTAMP DEFAULT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_habit(username, habit, frequency):
    """Add a new habit to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits WHERE username = ? AND habit = ?", (username, habit))
    existing = cursor.fetchone()

    if existing:
        print(f"'{habit}' already exists for {username}. Skipping insertion.")
    else:
        cursor.execute("INSERT INTO habits (username, habit, frequency) VALUES (?, ?, ?)",
                       (username, habit, frequency))
        conn.commit()
        print(f"Added '{habit}' for {username}")

    conn.close()

def mark_habit_done(username, habit):
    """Mark a habit as done for the current date."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE habits
        SET last_done = CURRENT_TIMESTAMP
        WHERE username = ? AND habit = ?
    """, (username, habit))
    conn.commit()

    message = (
        f"'{habit}' marked as done for {username}."
        if cursor.rowcount > 0
        else f"⚠️ No habit named '{habit}' found for {username}."
    )

    conn.close()
    return message

def is_habit_due(created_at, frequency, last_done=None):
    """Determine if a habit is due based on frequency."""
    date_to_check = last_done or created_at
    created_date = datetime.strptime(date_to_check, "%Y-%m-%d %H:%M:%S")
    days_passed = (datetime.now() - created_date).days

    freq_days = {
        "daily": 1,
        "every 2 days": 2,
        "weekly": 7,
        "biweekly": 14,
        "monthly": 30
    }
    return days_passed >= freq_days.get(frequency, 1)

def get_habits(username):
    """Retrieve all habits for a specific user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, habit, frequency, created_at, last_done FROM habits WHERE username = ?", (username,))
    rows = cursor.fetchall()
    conn.close()

    result = []
    for habit_id, habit, frequency, created_at, last_done in rows:
        if is_habit_due(created_at, frequency, last_done):
            reminder = f"⏰ Reminder: It's time to do your '{habit}' habit ({frequency})."
            status_icon = "❌"
        else:
            reminder = "✅ You're on track!"
            status_icon = "✅"

        result.append({
            "id": habit_id,
            "habit": f"{status_icon} {habit}",
            "frequency": frequency,
            "created_at": created_at,
            "last_done": last_done,
            "reminder": reminder
        })
    return result

if __name__ == "__main__":
    create_table()

