"""Alarms Service."""

from waylay.sdk import ApiClient, WaylayService

from ..api.alarm_events_api import AlarmEventsApi
from ..api.alarms_api import AlarmsApi
from ..api.alarms_batch_operations_api import AlarmsBatchOperationsApi
from ..api.version_api import VersionApi


class AlarmsService(WaylayService):
    """Alarms Service Class."""

    name = "alarms"
    title = "Alarms Service"

    alarm_events: AlarmEventsApi
    alarms: AlarmsApi
    alarms_batch_operations: AlarmsBatchOperationsApi
    version: VersionApi

    def __init__(self, api_client: ApiClient):
        """Create the alarms service."""

        super().__init__(api_client)
        self.alarm_events = AlarmEventsApi(api_client)
        self.alarms = AlarmsApi(api_client)
        self.alarms_batch_operations = AlarmsBatchOperationsApi(api_client)
        self.version = VersionApi(api_client)
