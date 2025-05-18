from typing import Optional
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from .tools import get_padel_court_availability
from datetime import datetime
from google.genai import types


def set_current_date_and_day_of_week(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """
    Logs entry and checks 'skip_llm_agent' in session state.
    If True, returns Content to skip the agent's execution.
    If False or not present, returns None to allow execution.
    """
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()

    print(f"\n[Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback] Current State: {current_state}")

    callback_context.state["temp:todays_date"] = datetime.now().strftime("%Y-%m-%d")
    callback_context.state["temp:todays_day_of_week"] = datetime.now().strftime("%A")

    return None


# Define the padel court manager agent
padel_court_agent = LlmAgent(
    model="gemini-2.0-flash",  # Using Gemini model
    name="padel_court_manager",
    description="Provides information about court availability",
    instruction="""You are a helpful agent that manages padel court bookings.

When a user asks about court availability:
1. Always make sure you have a specific date to check, if the date is not provided try to figure out what the date is from the user input.
2. Check the requested date
3. Provide information about which courts are available

Things to keep in mind:
- always use the current date and day of week to calculate the date
- user might asks for availability for a specific date that is either today or in the future
- user might ask for availability for a specific time slot

## Relative Dates considerations

User might ask for vauge date like "this Sunday", "next week", "next month". You need to convert theese into a specific date.

For example:

Input: "this Sunday"
State:
    temp:todays_date = 2025-05-17
    temp:todays_day_of_week = "Saturday"
Output: 2025-05-18
Explanation:
    The current day is Saturday 2025-05-17, so the next Sunday is one day after today, which is 2025-05-18

Always be polite and professional in your responses.

After you answer queries about padel court availability, return to the personal_assistant agent.
Any questions that you can't answer, you should return to the personal_assistant agent and let it answer.
""",
    output_key="court_availability_result",
    tools=[
        get_padel_court_availability,
    ],
    before_agent_callback=set_current_date_and_day_of_week,
)
