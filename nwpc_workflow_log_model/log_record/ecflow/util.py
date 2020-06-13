from enum import Enum

from nwpc_workflow_log_model.log_record import LogType


def convert_ecflow_log_type(log_type: str) -> LogType:
    """
    Get common log type from ecflow log's log type.

    Parameters
    ----------
    log_type: str
        log type in ecflow log record. Such as "LOG", "MSG", ...

    Returns
    -------
    LogType
    """
    log_type_mapper = {
        "LOG": LogType.Log,
        "MSG": LogType.Message,
        "DBG": LogType.Debug,
        "ERR": LogType.Error,
        "WAR": LogType.Warning,
    }
    return log_type_mapper.get(log_type, LogType.Unknown)


class EventType(Enum):
    Status = "status"
    Client = "client"
    Child = "child"
    Server = "server"
    Unknown = "unknown"
