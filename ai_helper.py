import requests

ZEN_QUOTE_URL = "https://zenquotes.io/api/random"

def get_motivational_quote():
    """Fetch a motivational quote from ZenQuotes API.
    If it fails, return a fallback message."""
    try:
        response = requests.get(ZEN_QUOTE_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            return f'"{data["q"]}" - {data["a"]}'
    except Exception as e:
        print(f"Error occurred: {e}")
    return "💡 Keep going — small, consistent steps lead to big change and even closer to your bigger goal!"

