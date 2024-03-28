from perceptinsight.constants import DEFAULT_INIT_OPTIONS
from perceptinsight.models import InitOptions, TrackingEventRequest, UserProperties, TrackingUserRequest
from typing import Any, List, Optional, Dict
from datetime import datetime
import copy
import asyncio
import logging
from threading import Timer

from perceptinsight.utils import get_modified_event_data, send_events, capture_user_properties


class PerceptInsight:
    logging.basicConfig(level=logging.DEBUG)
    __logger = logging.getLogger('PI')

    __is_sdk_initialized = False
    __time_threshold_milliseconds: int
    __batch_size: int
    __max_api_retry: int
    __batch_check_timer: Optional[Timer] = None
    __batched_event_requests: List[TrackingEventRequest]

    __token: Optional[str]

    def __init__(self):
        self.__time_threshold_milliseconds = 5000
        self.__batch_size = 1
        self.__batch_check_timer = None
        self.__batched_event_requests = []
        self.__max_api_retry = 2

    def initialize(self, token: str, init_options: InitOptions = InitOptions()):
        if self.__is_sdk_initialized:
            self.__logger.warning("Percept SDK has already been initialized. This call will be ignored")
            return

        if token is None or len(token.strip()) == 0:
            raise Exception("Percept token is mandatory for initializing the SDK")

        self.__token = token

        options = {**DEFAULT_INIT_OPTIONS.__dict__, **init_options.__dict__}

        self.__batch_size = options.get('autoFlushBatchSize', self.__batch_size)
        self.__time_threshold_milliseconds = options.get("autoFlushThresholdMs", self.__time_threshold_milliseconds)
        self.__max_api_retry = options.get("maxApiRetry", self.__max_api_retry)

        self.__is_sdk_initialized = True

    def set_user_properties(self, user_id: str, properties: UserProperties):
        self.__logger.info("Setting user properties")
        if not self.__can_process_requests():
            return

        if len(user_id.strip()) == 0:
            self.__logger.warning("[PI] can not set user properties without user id")
            return

        formatted_properties = get_modified_event_data(properties)
        asyncio.run(
            capture_user_properties(TrackingUserRequest(userId=user_id, data=formatted_properties.get("data", None),
                                                        multiData=formatted_properties.get("multiData", None)),
                                    token=self.__token, max_retry_count=self.__max_api_retry))

    def flush_pending_events(self):
        if len(self.__batched_event_requests) > 0:
            asyncio.run(self.__send_batched_api_calls_with_retry())

    def __clear_timer(self):
        if self.__batch_check_timer:
            self.__batch_check_timer.cancel()
            self.__batch_check_timer = None

    def __start_timer(self):
        self.__clear_timer()
        self.__batch_check_timer = Timer(self.__time_threshold_milliseconds / 1000, self.flush_pending_events)
        self.__batch_check_timer.start()

    def shut_down(self):
        self.flush_pending_events()
        self.__token = None
        return

    async def __send_batched_api_calls_with_retry(self):
        async def send_batched_calls():
            events_to_send = copy.deepcopy(self.__batched_event_requests)
            self.__batched_event_requests = []
            try:
                self.__clear_timer()
                await send_events(events_to_send, self.__token, self.__max_api_retry)
            except Exception as e:
                pass
            finally:
                return None

        if not self.__token:
            self.__logger.warning("Percept token is missing. You might have missed initializing the SDK")
            return
        return await send_batched_calls()

    def capture(self, event_name: str, user_id: Optional[str] = None, properties: Optional[Dict[str, Any]] = None):
        if not self.__can_process_requests():
            return
        try:
            properties = properties or {}
            properties.update({
                "user_id": user_id,
                "pi_client_ts": int(datetime.now().timestamp() * 1000),  # Convert to milliseconds
                "pi_sdk_type": 'python'
            })

            event_data = get_modified_event_data(properties)
            self.__batched_event_requests.append(TrackingEventRequest(name=event_name, data=event_data.get("data"),
                                                                      multiData=event_data.get("multiData")))

            if len(self.__batched_event_requests) >= self.__batch_size:
                asyncio.run(self.__send_batched_api_calls_with_retry())
            else:
                self.__start_timer()
        except Exception as e:
            pass

    def __is_initialized_with_token(self) -> bool:
        return self.__is_sdk_initialized and self.__token is not None

    def __can_process_requests(self) -> bool:
        if not self.__is_initialized_with_token():
            self.__logger.warning("Percept token is missing. You might have missed initializing the SDK")
            return False
        return True
