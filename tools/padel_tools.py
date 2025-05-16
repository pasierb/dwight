import requests
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import date, time, timedelta, datetime
from google.adk.tools import ToolContext

PM5_CHAM_TENANT_ID = "4a376db7-d434-4454-9827-34df7c7594ab"
PM5_CHAM_COURTS_MAP = {
    "8bdc9062-6d47-4f54-b830-3a3d270170e0": "Court 1",
    "0bb5e54b-37ff-4db9-9f54-fdc5892ee220": "Court 2",
    "3f569be5-df7c-48f0-bfa5-30ef9b920f91": "Court 3",
}

DATE_FORMAT = "%Y-%m-%d"


class Slot(BaseModel):
    start_time: time = Field(description="Start time in GMT")
    duration: int = Field(description="Duration in minutes")
    price: str = Field(description="Price in format 'VALUE CURRENCY', e.g. '92.5 CHF'")

    def to_dict(self, slot_date: date) -> Dict[str, Any]:
        start_time = datetime.combine(slot_date, self.start_time) + timedelta(hours=2)

        return {
            "start_time": (start_time).strftime("%H:%M"),
            "duration_in_minutes": self.duration,
            "price": self.price,
        }


class Resource(BaseModel):
    resource_id: str
    start_date: date
    slots: List[Slot]

    @property
    def name(self) -> str:
        return PM5_CHAM_COURTS_MAP[self.resource_id]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "start_date": self.start_date.strftime(DATE_FORMAT),
            "slots": [slot.to_dict(slot_date=self.start_date) for slot in self.slots],
        }


def __fetch_availability(date: date) -> List[Resource]:
    base_url = "https://playtomic.com/api/clubs/availability"
    params = {
        "tenant_id": PM5_CHAM_TENANT_ID,
        "date": date.strftime(DATE_FORMAT),
        "sport_id": "PADEL",
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            return []

        return [Resource.model_validate(court) for court in data]

    except requests.RequestException as e:
        raise Exception(f"Error fetching availability: {str(e)}")


def get_padel_court_availability(
    date_as_string: str, tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Get the availability of padel courts for a given date.

    Args:
        date_as_string (str): The date to check availability for in YYYY-MM-DD format

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status: str - The status of the operation ("success" or "error")
            - data: List[Dict[str, Any]] - List of dictionaries containing court availability information
            - error_message: str - Optional error message if status is "error"
    """
    try:
        date_value = date.fromisoformat(date_as_string)
    except ValueError:
        return {
            "status": "error",
            "error_message": f"Invalid date format. Please use {DATE_FORMAT} format.",
            "data": [],
        }

    try:
        availability = __fetch_availability(date_value)
        data = [resource.to_dict() for resource in availability]

        return {
            "status": "success",
            "data": data,
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e), "data": []}
