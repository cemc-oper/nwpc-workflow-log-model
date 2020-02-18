from loguru import logger

from nwpc_workflow_log_model.log_record.ecflow.util import EventType, convert_ecflow_log_type
from nwpc_workflow_log_model.log_record.log_record import LogRecord, LogType


class EcflowLogRecord(LogRecord):
    def __init__(
            self,
            log_type=LogType.Unknown,
            date=None,
            time=None,
            log_record=None):
        LogRecord.__init__(self)
        self.log_type = log_type
        self.log_record = log_record
        self.date = date
        self.time = time
        self.event_type: EventType = EventType.Unknown
