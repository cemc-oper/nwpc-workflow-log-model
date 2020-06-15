import datetime

from loguru import logger

from .record import EcflowLogRecord, LogType, EventType


class ServerLogRecord(EcflowLogRecord):
    def __init__(
            self,
            log_type: LogType = LogType.Unknown,
            date: datetime.date = None,
            time: datetime.time = None,
            log_record: str = None
    ):
        EcflowLogRecord.__init__(
            self,
            log_type=log_type,
            date=date,
            time=time,
            log_record=log_record
        )
        self.event_type = EventType.Server
        self.command = None

    def parse_record(
            self,
            line: str,
            debug: bool = False
    ):
        start_pos = 0
        end_pos = line.find(" ", start_pos)
        if end_pos == -1:
            if debug:
                logger.error(f"[ERROR] child record: event not found => {self.log_record}")
            return
        event = line[start_pos:end_pos]
        self.event = event
        self.command = self.event
