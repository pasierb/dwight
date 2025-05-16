from google.adk.agents import Agent
from .prompts import system_prompt
from tools import get_padel_court_availability

root_agent = Agent(
    name="personal_assistant",
    model="gemini-2.0-flash",
    description="The root agent for the Dwight project",
    instruction=system_prompt,
    tools=[get_padel_court_availability],
)

