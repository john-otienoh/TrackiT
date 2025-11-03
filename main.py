from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Optional
from habit_manager import get_user_habits_with_quote, create_user_habit
from database import mark_habit_done, create_table
import uvicorn

app = FastAPI(title="Habit Tracker API", version="2.0.0")
create_table()

class HabitCreate(BaseModel):
    habit: str
    frequency: str

class HabitMark(BaseModel):
    habit: str

@app.get("/habits/{username}")
def list_habits(username: str):
    return get_user_habits_with_quote(username)

@app.post("/habits/{username}")
def create_habit(username: str, data: HabitCreate):
    response, status = create_user_habit(username, data.habit, data.frequency)
    if status != 201:
        raise HTTPException(status_code=status, detail=response["error"])
    return response

@app.post("/habits/{username}/mark_done")
def mark_done(username: str, data: HabitMark):
    message = mark_habit_done(username, data.habit)
    return {"message": message}

@app.post("/a2a/habits")
def a2a_habits(body: dict = Body(...)):
    """JSON-RPC 2.0 compatible endpoint."""
    try:
        if body.get("jsonrpc") != "2.0" or "id" not in body or "method" not in body:
            raise HTTPException(status_code=400, detail="Invalid JSON-RPC request")

        rpc_id = body["id"]
        method = body["method"]
        params = body.get("params", {})

        username = params.get("username")
        if not username:
            raise HTTPException(status_code=400, detail="Missing 'username' parameter")

        if method == "habits/get":
            result = get_user_habits_with_quote(username)
        elif method == "habits/add":
            habit = params.get("habit")
            frequency = params.get("frequency")
            if not habit or not frequency:
                raise HTTPException(status_code=400, detail="Missing 'habit' or 'frequency' parameter")
            result, _ = create_user_habit(username, habit, frequency)
        elif method == "habits/mark_done":
            habit = params.get("habit")
            if not habit:
                raise HTTPException(status_code=400, detail="Missing 'habit' parameter")
            message = mark_habit_done(username, habit)
            result = {"message": message}
        else:
            raise HTTPException(status_code=404, detail=f"Method '{method}' not found")

        return {"jsonrpc": "2.0", "id": rpc_id, "result": result}

    except HTTPException as e:
        return {"jsonrpc": "2.0", "id": body.get("id"), "error": {"code": e.status_code, "message": e.detail}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": body.get("id"), "error": {"code": -32603, "message": "Internal error", "data": str(e)}}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

