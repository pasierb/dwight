from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .prompts import system_prompt
from .sub_agents import padel_court_agent

root_agent = Agent(
    name="personal_assistant",
    model="gemini-2.0-flash",
    description="The root agent for the Dwight project",
    instruction=system_prompt,
    tools=[],
    sub_agents=[padel_court_agent],
)
