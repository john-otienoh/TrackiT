from database import add_habit, get_habits
from ai_helper import get_motivational_quote

def get_user_habits_with_quote(username):
    habits = get_habits(username)
    quote = get_motivational_quote()
    return {"habits": habits, "motivational_quote": quote}

def create_user_habit(username, habit_name, frequency):
    if not habit_name or not frequency:
        return {"error": "Habit and frequency are required"}, 400

    add_habit(username, habit_name, frequency)
    return {"message": f"Habit '{habit_name}' added for user {username}."}, 201

