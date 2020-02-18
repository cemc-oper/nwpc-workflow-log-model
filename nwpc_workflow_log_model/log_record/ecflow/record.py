from ..log_record import LogRecord, LogType
from .util import EventType


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

    def parse(self, line: str):
        raise NotImplemented("Please use EcflowLogParser to parse logs.")
