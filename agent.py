import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import requests

def get_apod() -> dict:
    """Gets the picture of the day.

    
    Returns:
        picture of day.
    """
    api_key = "Put your api kye here"
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "status" : "success",
            "title" : data["title"],
            "image_url" : data["url"],
            "explaination" : data["explanation"]
        }
    else:
        return {
            "status": "error",
            "error_message": f"Picture could not be provided",
        }
   


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


root_agent = Agent(
    name="pod_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to give today's astronomy picture of the day"
    ),
    instruction=(
        "You are a helpful agent who can provide todays picture of day"
    ),
    tools=[get_apod],
)