from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from habit_manager import create_user_habit, get_user_habits_with_quote
from database import create_table, mark_habit_done

app = FastAPI(title="Motivational Habit Tracker API")
create_table()

class HabitCreate(BaseModel):
    habit: str
    frequency: str


@app.post("/habits/{username}")
async def add_habit(username: str, habit_data: HabitCreate):
    """
    Add a new habit for a user.
    Example:
    POST /habits/john
    {
      "habit": "Read 10 pages",
      "frequency": "daily"
    }
    """
    try:
        habit_name = habit_data.habit
        frequency = habit_data.frequency
        response, status = create_user_habit(username, habit_name, frequency)
        return JSONResponse(content=response, status_code=status)

    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to create habit: {str(e)}"},
            status_code=500
        )

@app.get("/habits/{username}")
async def list_habits(username: str):
    """
    Retrieve all habits for a user, including motivational quote.
    Example:
    GET /habits/john
    """
    try:
        result = get_user_habits_with_quote(username)
        if not result["habits"]:
            return JSONResponse(
                content={"message": f"No habits found for user {username}."},
                status_code=404
            )
        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to fetch habits: {str(e)}"},
            status_code=500
        )

class HabitMarkDone(BaseModel):
    habit: str


@app.post("/habits/{username}/mark_done")
async def mark_done(username: str, habit_data: HabitMarkDone):
    """
    Mark a habit as done for a specific user.
    Example:
    POST /habits/john/mark_done
    {
      "habit": "Read 10 pages"
    }
    """
    try:
        habit_name = habit_data.habit
        message = mark_habit_done(username, habit_name)
        return JSONResponse(content={"message": message}, status_code=200)

    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to mark habit as done: {str(e)}"},
            status_code=500
        )

@app.post("/a2a/habits")
async def a2a_habits(request: Request):
    try:
        try:
            body = await request.json()
        except Exception:
            return JSONResponse(
                status_code=400,
                content={
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error: Request body is empty or invalid JSON."
                    },
                },
            )
        if body.get("jsonrpc") != "2.0" or "id" not in body or "method" not in body:
            return JSONResponse(
                status_code=400,
                content={
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request: jsonrpc must be '2.0', and 'id' and 'method' are required"
                    },
                },
            )

        rpc_id = body["id"]
        method = body["method"]
        params = body.get("params", {})

        username = params.get("username")
        if not username:
            return JSONResponse(
                status_code=400,
                content={
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "error": {"code": -32602, "message": "Missing 'username' parameter"},
                },
            )
        if method == "habits/get":
            result = get_user_habits_with_quote(username)

        elif method == "habits/add":
            habit = params.get("habit")
            frequency = params.get("frequency")
            if not habit or not frequency:
                return JSONResponse(
                    status_code=400,
                    content={
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "error": {"code": -32602, "message": "Missing 'habit' or 'frequency' parameter"},
                    },
                )
            result, _ = create_user_habit(username, habit, frequency)

        elif method == "habits/mark_done":
            habit = params.get("habit")
            if not habit:
                return JSONResponse(
                    status_code=400,
                    content={
                        "jsonrpc": "2.0",
                        "id": rpc_id,
                        "error": {"code": -32602, "message": "Missing 'habit' parameter"},
                    },
                )
            message = mark_habit_done(username, habit)
            result = {"message": message}

        else:
            return JSONResponse(
                status_code=404,
                content={
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "error": {"code": -32601, "message": f"Method '{method}' not found"},
                },
            )

        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": result,
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "id": body.get("id") if "body" in locals() else None,
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e),
                },
            },
        )
