from loguru import logger

from nwpc_workflow_log_model.log_record.ecflow.util import EventType
from nwpc_workflow_log_model.log_record.ecflow.record import EcflowLogRecord


class EcflowLogParser(object):
    def __init__(self):
        pass

    def parse(self, line: str) -> EcflowLogRecord:
        log_record = EcflowLogRecord()
        log_record.log_record = line

        start_pos = 0
        end_pos = line.find(":")
        log_record._parse_log_type(line[start_pos:end_pos])

        start_pos = end_pos + 2
        end_pos = line.find("]", start_pos)
        if end_pos == -1:
            logger.warning("can't find date and time => ", line)
            return log_record
        log_record._parse_datetime(line[start_pos:end_pos])

        start_pos = end_pos + 2
        if line[start_pos: start_pos + 1] == " ":
            log_record.event_type = EventType.Status
            start_pos += 1
            log_record._parse_status_record(line[start_pos:])
        elif line[start_pos: start_pos + 2] == "--":
            log_record.event_type = EventType.Client
            start_pos += 2
            log_record._parse_client_record(line[start_pos:])
        elif line[start_pos: start_pos + 4] == "chd:":
            # child event
            log_record.event_type = EventType.Child
            start_pos += 4
            log_record._parse_child_record(line[start_pos:])
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
