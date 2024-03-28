from collections import defaultdict
from typing import Dict, Any, List

import requests
import logging

from perceptinsight.constants import USER_TRACKING_ENDPOINT, EVENT_TRACKING_ENDPOINT
from perceptinsight.models import TrackingEventRequest, TrackingUserRequest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('PI')


def get_modified_event_data(properties=None) -> Dict[str, Any]:
    if properties is None:
        properties = {}
    string_properties: Dict[str, str] = {}
    list_properties: Dict[str, List[str]] = defaultdict(list)

    for key, value in properties.items():
        if isinstance(value, list):
            list_properties[key] = value
        elif value is None:
            pass
        else:
            string_properties[key] = str(value)

    return {
        "data": string_properties,
        "multiData": dict(list_properties)
    }


async def send_user_request(url: str, token: str, body: TrackingUserRequest):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': f'Bearer {token}',
    }
    body = body.to_dict()
    response = requests.post(url, headers=headers, json=body)
    return response


async def send_events(events: List[TrackingEventRequest], token: str, max_retry_count=2):
    retry_count = 0
    is_success = False

    while retry_count < max_retry_count and not is_success:
        try:
            await send_events_executor(events, token)
            is_success = True
        except Exception as error:
            retry_count += 1
            if retry_count == max_retry_count:
                logger.warning("[PI] api call failed. setting up retry with exponential backoff")
                logger.warning("[PI]: api failure error:", error)


async def send_events_executor(events: List[TrackingEventRequest], token: str):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': f'Bearer {token}',
    }
    data = {
        "events": [event.to_dict() for event in events],
    }
    response = requests.post(EVENT_TRACKING_ENDPOINT, headers=headers, json=data)
    response.raise_for_status()


async def capture_user_properties(body: TrackingUserRequest, token: str, max_retry_count=2):
    retry_count = 0
    is_success = False

    while retry_count < max_retry_count and not is_success:
        try:
            response = await send_user_request(USER_TRACKING_ENDPOINT, token, body)
            response.raise_for_status()
            is_success = True
        except Exception as error:
            retry_count += 1
            if retry_count == max_retry_count:
                logger.warning("[PI] user properties api call failed.")
                logger.warning("[PI] please try setting this after some time:", body)
