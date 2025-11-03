# TrackiT
A simple **AI-powered habit tracking API** built with **FastAPI**, **SQLite**, and **ZenQuotes** for motivational quotes.
---

### 🚀 Features

✅ Add, list, and mark habits as done</br>
✅ JSON-RPC 2.0 compatible endpoint for programmatic integrations</br>
✅ AI helper that fetches motivational quotes from [ZenQuotes API](https://zenquotes.io/)</br>
✅ Smart reminders based on habit frequency (daily, weekly, biweekly, etc.)</br>
✅ SQLite lightweight persistence</br>
✅ Simple and clean API design using FastAPI</br>

---

### 🏗️ Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** SQLite
* **Motivational AI:** ZenQuotes API
* **Runtime:** Uvicorn

---

### 📁 Project Structure

```
HNG_Stage_3_fastapi/
│
├── ai_helper.py          # Fetches motivational quotes from ZenQuotes
├── database.py           # Handles SQLite database logic
├── habit_manager.py      # Business logic layer
├── main.py               # FastAPI application entry point
└── requirements.txt      # Python dependencies
```

---

### ⚙️ Installation & Setup

#### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/HNG_Stage_3_fastapi.git
cd HNG_Stage_3_fastapi
```

#### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

#### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Run the app

```bash
uvicorn main:app --reload
```

App will start on:

```
http://127.0.0.1:8000
```

---

### 📬 API Endpoints

#### ➕ Add Habit

**POST** `/habits/{username}`
Request body:

```json
{
  "habit": "Read 10 pages",
  "frequency": "daily"
}
```

Response:

```json
{
  "message": "Habit 'Read 10 pages' added for user john."
}
```

---

#### 📋 List Habits (with AI Quote)

**GET** `/habits/{username}`
Response:

```json
{
  "habits": [
    {
      "id": 1,
      "habit": "✅ Read 10 pages",
      "frequency": "daily",
      "created_at": "2025-11-03 09:00:00",
      "last_done": "2025-11-02 09:00:00",
      "reminder": "✅ You're on track!"
    }
  ],
  "motivational_quote": "\"Discipline equals freedom.\" - Jocko Willink"
}
```

---

#### ✅ Mark Habit as Done

**POST** `/habits/{username}/mark_done`
Request body:

```json
{
  "habit": "Read 10 pages"
}
```

Response:

```json
{
  "message": "✅ 'Read 10 pages' marked as done for john."
}
```

---

### 🤖 JSON-RPC Support

**POST** `/a2a/habits`

Example request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "habits/get",
  "params": { "username": "john" }
}
```

Example response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "habits": [...],
    "motivational_quote": "\"The best way to get started is to quit talking and begin doing.\" - Walt Disney"
  }
}
```

Supported `method` values:

* `habits/get`
* `habits/add`
* `habits/mark_done`

---

### 🧩 Supported Frequencies

| Frequency      | Interval (Days) |
| -------------- | --------------- |
| `daily`        | 1               |
| `every 2 days` | 2               |
| `weekly`       | 7               |
| `biweekly`     | 14              |
| `monthly`      | 30              |

---

### 🌐 Deployment

You can deploy easily to:

* **[Railway](https://railway.app)**
Example `Procfile` for Railway:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

### 👨‍💻 Author

**John Charles**
🚀 Built for HNG Stage 3 Challenge

---
