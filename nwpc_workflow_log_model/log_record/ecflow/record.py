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

        self.event_type: EventType = EventType.Unknown

    def parse(self, line: str):
        """
        NOTE
        ----
            ERR:[02:23:59 10.1.2020] Connection::handle_read_data, boost::archive::archive_exception unsupported version, in server
            ERR:[02:23:59 10.1.2020] 22 serialization::archive 17 0 0 0 1 2 8 CSyncCmd 1 0
            ERR:[02:23:59 10.1.2020] 0 0 0 0 0 4 root 2 0 0 0, in server
            ERR:[02:23:59 10.1.2020] Connection::handle_read_data archive version miss-match!, in server
        """
        self.log_record = line

        start_pos = 0
        end_pos = line.find(":")
        self._parse_log_type(line[start_pos:end_pos])

        start_pos = end_pos + 2
        end_pos = line.find("]", start_pos)
        if end_pos == -1:
            logger.warning("can't find date and time => ", line)
            return
        self._parse_datetime(line[start_pos:end_pos])

        start_pos = end_pos + 2
        if line[start_pos: start_pos + 1] == " ":
            self.event_type = EventType.Status
            start_pos += 1
            self._parse_status_record(line[start_pos:])
        elif line[start_pos: start_pos + 2] == "--":
            self.event_type = EventType.Client
            start_pos += 2
            self._parse_client_record(line[start_pos:])
        elif line[start_pos: start_pos + 4] == "chd:":
            # child event
            self.event_type = EventType.Child
            start_pos += 4
            self._parse_child_record(line[start_pos:])
        elif line[start_pos: start_pos + 4] == "svr:":
            # server
            # print("[server event]", line)
            self.event_type = EventType.Server
        elif len(line[start_pos:].strip()) > 0:
            # NOTE: line[start_pos].strip() will be empty but I haven't found example line.
            if line[start_pos:].strip()[0].isupper():
                # WAR:[09:00:08 6.8.2018] Job generation for task /grapes_emer_v1_1/00/plot/get_plot/get_plot_meso
                #  took 4593ms, Exceeds ECF_TASK_THRESHOLD(4000ms)
                pass
            else:
                pass
        else:
            # not supported
            # print("[not supported]", line)
            pass

        return self

    def _parse_log_type(self, token: str):
        self.log_type = convert_ecflow_log_type(token)


