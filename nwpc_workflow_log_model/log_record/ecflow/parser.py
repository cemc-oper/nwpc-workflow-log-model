import datetime

from loguru import logger

from nwpc_workflow_log_model.log_record import LogType

from .record import EcflowLogRecord
from .status_record import StatusLogRecord
from .client_record import ClientLogRecord
from .child_record import ChildLogRecord
from .server_record import ServerLogRecord
from .util import convert_ecflow_log_type, EventType, merge_dict


class EcflowLogParser(object):
    def __init__(self, options: dict = None):
        self.options = {
            "parser": {
                "debug": False,
            },
            EventType.Status: {
                "debug": False,
                "enable": True,
            },
            EventType.Client: {
                "debug": False,
                "enable": True,
            },
            EventType.Child: {
                "debug": False,
                "enable": True,
            },
            EventType.Server: {
                "debug": False,
                "enable": True,
            }
        }
        if options is not None:
            merge_dict(self.options, options)

    def disable_event_parse(self, event_type):
        self.options[event_type]["enable"] = False

    def enable_event_parse(self, event_type):
        self.options[event_type]["enable"] = True

    def parse(self, line: str) -> EcflowLogRecord:
        """
        Parse ecflow log line.

        Parameters
        ----------
        line: str
            log line.

        Returns
        -------
        EcflowLogRecord
            if log line can't be parsed, return a default empty EcflowLogRecord object.
        """
        log_record = EcflowLogRecord(log_record=line)

        start_pos = 0
        end_pos = line.find(":")
        log_type_token = line[start_pos:end_pos]
        log_type = self._parse_log_type(log_type_token)
        log_record.log_type = log_type

        start_pos = end_pos + 2
        end_pos = line.find("]", start_pos)
        if end_pos == -1:
            logger.warning(f"can't find date and time => {line}")
            return log_record

        date_time_token = line[start_pos:end_pos]

        start_pos = end_pos + 2
        if line[start_pos: start_pos + 1] == " ":
            if not self.options[EventType.Status]["enable"]:
                return log_record
            date_time = self._parse_datetime(date_time_token)
            log_record = StatusLogRecord(
                log_type=log_type,
                date=date_time.date(),
                time=date_time.time(),
                log_record=line,
            )
            start_pos += 1
            log_record.parse_record(
                line[start_pos:],
                debug=self.options[EventType.Status]["debug"],
            )
        elif line[start_pos: start_pos + 2] == "--":
            if not self.options[EventType.Client]["enable"]:
                return log_record
            date_time = self._parse_datetime(date_time_token)
            log_record = ClientLogRecord(
                log_type=log_type,
                date=date_time.date(),
                time=date_time.time(),
                log_record=line,
            )
            start_pos += 2
            log_record.parse_record(
                line[start_pos:],
                debug=self.options[EventType.Client]["debug"],
            )
        elif line[start_pos: start_pos + 4] == "chd:":
            # child event
            if not self.options[EventType.Child]["enable"]:
                return log_record
            date_time = self._parse_datetime(date_time_token)
            log_record = ChildLogRecord(
                log_type=log_type,
                date=date_time.date(),
                time=date_time.time(),
                log_record=line,
            )
            start_pos += 4
            log_record.parse_record(
                line[start_pos:],
                debug=self.options[EventType.Child]["debug"],
            )
        elif line[start_pos: start_pos + 4] == "svr:":
            # server
            # MSG:[05:41:25 2.2.2020] svr:check_pt in 0 seconds
            if not self.options[EventType.Server]["enable"]:
                return log_record
            date_time = self._parse_datetime(date_time_token)
            log_record = ServerLogRecord(
                log_type=log_type,
                date=date_time.date(),
                time=date_time.time(),
                log_record=line,
            )
            start_pos += 4
            log_record.parse_record(
                line[start_pos:],
                debug=self.options[EventType.Server]["debug"],
            )
        elif len(line[start_pos:].strip()) > 0:
            # date_time = self._parse_datetime(date_time_token)
            # log_record.date = date_time.date()
            # log_record.time = date_time.time()

            # NOTE: line[start_pos].strip() will be empty but I haven't found example line.
            if line[start_pos:].strip()[0].isupper():
                # WAR:[09:00:08 6.8.2018] Job generation for task /grapes_emer_v1_1/00/plot/get_plot/get_plot_meso
                #  took 4593ms, Exceeds ECF_TASK_THRESHOLD(4000ms)
                pass
            else:
                pass
        else:
            # date_time = self._parse_datetime(date_time_token)
            # log_record.date = date_time.date()
            # log_record.time = date_time.time()

            # not supported
            # print("[not supported]", line)
            pass

        return log_record

    def _parse_log_type(self, token: str) -> LogType:
        log_type = convert_ecflow_log_type(token)
        return log_type

    def _parse_datetime(self, token: str) -> datetime.datetime:
        date_time = datetime.datetime.strptime(token, "%H:%M:%S %d.%m.%Y")
        return date_time
