from datetime import datetime

from loguru import logger

from nwpc_workflow_log_model.log_record.ecflow.util import EventType, convert_ecflow_log_type
from nwpc_workflow_log_model.log_record.ecflow.record import EcflowLogRecord
from nwpc_workflow_log_model.log_record.ecflow.status_record import StatusLogRecord
from nwpc_workflow_log_model.log_record.ecflow.client_record import ClientLogRecord
from nwpc_workflow_log_model.log_record.ecflow.child_record import ChildLogRecord


class EcflowLogParser(object):
    def __init__(self):
        pass

    def parse(self, line: str) -> EcflowLogRecord:
        log_record = EcflowLogRecord(log_record=line)

        start_pos = 0
        end_pos = line.find(":")
        log_type = self._parse_log_type(line[start_pos:end_pos])
        log_record.log_type = log_type

        start_pos = end_pos + 2
        end_pos = line.find("]", start_pos)
        if end_pos == -1:
            logger.warning("can't find date and time => ", line)
            return log_record
        date_time = self._parse_datetime(line[start_pos:end_pos])
        log_record.date = date_time.date()
        log_record.time = date_time.time()

        start_pos = end_pos + 2
        if line[start_pos: start_pos + 1] == " ":
            log_record = StatusLogRecord(
                log_type=log_type,
                date=date_time.date(),
                time=date_time.time(),
                log_record=line,
            )
            start_pos += 1
            log_record.parse_record(line[start_pos:])
        elif line[start_pos: start_pos + 2] == "--":
            log_record = ClientLogRecord(
                log_type=log_type,
                date=date_time.date(),
                time=date_time.time(),
                log_record=line,
            )
            start_pos += 2
            log_record.parse_record(line[start_pos:])
        elif line[start_pos: start_pos + 4] == "chd:":
            # child event
            log_record = ChildLogRecord(
                log_type=log_type,
                date=date_time.date(),
                time=date_time.time(),
                log_record=line,
            )
            start_pos += 4
            log_record.parse_record(line[start_pos:])
        elif line[start_pos: start_pos + 4] == "svr:":
            # server
            # print("[server event]", line)
            log_record.event_type = EventType.Server
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

        return log_record

    def _parse_log_type(self, token: str):
        log_type = convert_ecflow_log_type(token)
        return log_type

    def _parse_datetime(self, token: str):
        date_time = datetime.strptime(token, "%H:%M:%S %d.%m.%Y")
        return date_time
