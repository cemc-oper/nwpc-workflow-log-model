from enum import Enum
import collections

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


def merge_dict(d1, d2):
    for k, v2 in d2.items():
        v1 = d1.get(k)  # returns None if v1 has no value for this key
        if (
                isinstance(v1, collections.Mapping)
                and
                isinstance(v2, collections.Mapping)
        ):
            merge_dict(v1, v2)
        else:
            d1[k] = v2
