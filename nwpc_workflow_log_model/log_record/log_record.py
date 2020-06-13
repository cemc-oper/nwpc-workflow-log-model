from datetime import date, time
from enum import Enum


class LogType(Enum):
    Debug = "debug"
    Info = "info"
    Warning = "warn"
    Error = "error"
    Fatal = "fatal"

    Log = "log"
    Message = "message"
    Unknown = "unknown"


class LogRecord(object):
    def __init__(self):
        self.log_type: LogType = LogType.Unknown
        self.date: date or None = None
        self.time: time or None = None
        self.event: str or None = None
        self.node_path: str or None = None
        self.additional_attrs: dict = {}
        self.log_record: str or None = None

    def __str__(self):
        return f"{self.log_record}"

    def __repr__(self):
        return f"[{self.__class__.__name__}] {self.log_record}"

    def parse(self, line: str):
        pass
