from nwpc_workflow_log_model.log_record.log_record import LogType


def convert_ecflow_log_type(log_type: str) -> LogType:
    log_type_mapper = {
        "LOG": LogType.Log,
        "MSG": LogType.Message,
        "DBG": LogType.Debug,
        "ERR": LogType.Error,
        "WAR": LogType.Warning,
    }
    return log_type_mapper.get(log_type, LogType.Unknown)