from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from habit_manager import get_user_habits_with_quote, create_user_habit
from database import mark_habit_done, create_table
import os

app = FastAPI(title="Motivational Habit Tracker API")
create_table()


@app.get("/habits/{username}")
def list_habits(username: str):
    """Get all habits for a specific user, plus a motivational quote."""
    return get_user_habits_with_quote(username)


@app.post("/habits/{username}")
async def create_habit(username: str, request: Request):
    """Add a new habit for a specific user."""
    data = await request.json()
    habit_name = data.get("habit")
    frequency = data.get("frequency")

    response, status = create_user_habit(username, habit_name, frequency)
    return JSONResponse(content=response, status_code=status)


@app.post("/a2a/habits")
async def a2a_habits(request: Request):
    """Handle A2A JSON-RPC requests (Telex integration)."""
    try:
        body = await request.json()

        # ✅ Basic JSON-RPC structure validation
        if body.get("jsonrpc") != "2.0" or "id" not in body or "method" not in body:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": body.get("id"),
                "error": {
                    "code": -32600,
                    "message": "Invalid Request: jsonrpc must be '2.0', id and method are required"
                }
            }, status_code=400)

        rpc_id = body["id"]
        method = body["method"]
        params = body.get("params", {})
        username = params.get("username")

        if not username:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32602, "message": "Missing 'username' parameter"}
            }, status_code=400)

        # ✅ Handle supported methods
        if method == "habits/get":
            result = get_user_habits_with_quote(username)

        elif method == "habits/add":
            habit_name = params.get("habit")
            frequency = params.get("frequency")
            if not habit_name or not frequency:
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "error": {"code": -32602, "message": "Missing 'habit' or 'frequency' parameter"}
                }, status_code=400)
            result, _ = create_user_habit(username, habit_name, frequency)

        elif method == "habits/mark_done":
            habit_name = params.get("habit")
            if not habit_name:
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "error": {"code": -32602, "message": "Missing 'habit' parameter"}
                }, status_code=400)
            message = mark_habit_done(username, habit_name)
            result = {"message": message}

        else:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            }, status_code=404)

        # ✅ Return success response in JSON-RPC format
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": result
        })

    except Exception as e:
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id") if "body" in locals() else None,
            "error": {"code": -32603, "message": "Internal error", "data": str(e)}
        }, status_code=500)


@app.post("/habits/{username}/mark_done")
async def mark_done(username: str, request: Request):
    """Mark a habit as done."""
    data = await request.json()
    habit = data.get("habit")

    if not habit:
        raise HTTPException(status_code=400, detail="Please provide the saved habit name.")

    message = mark_habit_done(username, habit)
    return {"message": message}
